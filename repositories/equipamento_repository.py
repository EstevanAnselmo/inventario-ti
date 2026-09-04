"""
Camada de persistência.

Responsabilidade única: ler e gravar equipamentos em um meio físico
de armazenamento. Não conhece regras de negócio (duplicidade,
validação de campos obrigatórios etc.) — isso é responsabilidade da
camada de serviço.

EquipamentoRepository é um Protocol (interface estrutural): a camada
de serviço depende dessa abstração, não da implementação concreta em
JSON. Isso permite, por exemplo, trocar por um SqliteEquipamentoRepository
no futuro sem tocar em InventarioService, e permite testar o serviço
com um repositório falso em memória (ver tests/test_inventario_service.py).
"""

import json
import os
import tempfile
from typing import Dict, Protocol

from models import Equipamento
from exceptions import PersistenciaError, DadosInvalidosError


class EquipamentoRepository(Protocol):
    def carregar(self) -> Dict[str, Equipamento]:
        ...

    def salvar(self, equipamentos: Dict[str, Equipamento]) -> None:
        ...


class JsonEquipamentoRepository:
    """Implementação de EquipamentoRepository usando um arquivo JSON local."""

    def __init__(self, arquivo_db: str = "inventario.json"):
        self.arquivo_db = arquivo_db

    def carregar(self) -> Dict[str, Equipamento]:
        if not os.path.exists(self.arquivo_db):
            return {}

        try:
            with open(self.arquivo_db, "r", encoding="utf-8") as file:
                conteudo = file.read()
        except OSError as erro:
            raise PersistenciaError(f"Erro ao ler arquivo '{self.arquivo_db}': {erro}") from erro

        # Arquivo existente porém vazio (ex: criado manualmente com touch,
        # ou processo anterior interrompido antes de escrever) é um caso
        # de borda real: json.loads("") lançaria JSONDecodeError, então
        # tratamos explicitamente como "sem dados" em vez de erro fatal.
        if not conteudo.strip():
            return {}

        try:
            dados_brutos = json.loads(conteudo)
        except json.JSONDecodeError as erro:
            raise PersistenciaError(
                f"Arquivo '{self.arquivo_db}' contém JSON inválido: {erro}"
            ) from erro

        if not isinstance(dados_brutos, dict):
            raise PersistenciaError(
                f"Arquivo '{self.arquivo_db}' não contém um objeto JSON no formato esperado."
            )

        equipamentos: Dict[str, Equipamento] = {}
        for chave, valores in dados_brutos.items():
            try:
                equipamentos[chave] = Equipamento.from_dict(valores)
            except DadosInvalidosError as erro:
                # Um único registro corrompido derruba o carregamento inteiro
                # de propósito: continuar carregando "pela metade" mascararia
                # a corrupção e poderia levar a perda silenciosa de dados na
                # próxima gravação (o registro corrompido seria descartado
                # sem o usuário nunca saber).
                raise PersistenciaError(
                    f"Registro '{chave}' inválido em '{self.arquivo_db}': {erro}"
                ) from erro

        return equipamentos

    def salvar(self, equipamentos: Dict[str, Equipamento]) -> None:
        """
        Escrita atômica: grava em um arquivo temporário no mesmo
        diretório e só então substitui o arquivo final via os.replace()
        (atômico no mesmo filesystem). Se o processo for interrompido
        no meio da gravação, o inventario.json original permanece
        intacto — nunca fica em estado parcialmente escrito.
        """
        dados = {chave: eq.to_dict() for chave, eq in equipamentos.items()}
        diretorio = os.path.dirname(os.path.abspath(self.arquivo_db)) or "."

        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=diretorio, delete=False, suffix=".tmp"
            ) as tmp:
                json.dump(dados, tmp, ensure_ascii=False, indent=4)
                caminho_tmp = tmp.name
            os.replace(caminho_tmp, self.arquivo_db)
        except OSError as erro:
            raise PersistenciaError(f"Erro ao salvar arquivo '{self.arquivo_db}': {erro}") from erro
