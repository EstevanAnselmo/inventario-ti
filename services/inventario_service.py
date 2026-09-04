"""
Camada de serviço: regras de negócio do inventário.

Não conhece JSON, arquivo, terminal nem HTTP — só conhece o contrato
EquipamentoRepository (Protocol) e as regras do domínio. Isso é o que
permite reaproveitar essa classe inteira tanto na CLI quanto numa API
FastAPI sem duplicar nenhuma regra.
"""

from typing import Dict, List, Optional

from models import Equipamento, StatusEquipamento, TipoEquipamento
from repositories import EquipamentoRepository
from exceptions import (
    PatrimonioDuplicadoError,
    PatrimonioNaoEncontradoError,
    DadosInvalidosError,
)


class InventarioService:
    def __init__(self, repositorio: EquipamentoRepository):
        self._repositorio = repositorio
        self._equipamentos: Dict[str, Equipamento] = self._repositorio.carregar()

    @staticmethod
    def _normalizar(patrimonio: str) -> str:
        return patrimonio.strip().upper()

    @staticmethod
    def _validar_campos_obrigatorios(marca: str, modelo: str, usuario: str, setor: str) -> None:
        campos = {"marca": marca, "modelo": modelo, "usuario": usuario, "setor": setor}
        vazios = [nome for nome, valor in campos.items() if not valor or not valor.strip()]
        if vazios:
            raise DadosInvalidosError(
                f"Campo(s) obrigatório(s) vazio(s): {', '.join(vazios)}."
            )

    def adicionar(
        self,
        patrimonio: str,
        tipo: TipoEquipamento,
        marca: str,
        modelo: str,
        usuario: str,
        setor: str,
        status: StatusEquipamento = StatusEquipamento.ATIVO,
    ) -> Equipamento:
        chave = self._normalizar(patrimonio)
        if not chave:
            raise DadosInvalidosError("O patrimônio não pode estar vazio.")
        if chave in self._equipamentos:
            raise PatrimonioDuplicadoError(chave)

        self._validar_campos_obrigatorios(marca, modelo, usuario, setor)

        equipamento = Equipamento(
            patrimonio=chave,
            tipo=tipo,
            marca=marca.strip(),
            modelo=modelo.strip(),
            usuario=usuario.strip(),
            setor=setor.strip(),
            status=status,
        )
        self._equipamentos[chave] = equipamento
        self._repositorio.salvar(self._equipamentos)
        return equipamento

    def buscar(self, patrimonio: str) -> Optional[Equipamento]:
        return self._equipamentos.get(self._normalizar(patrimonio))

    def obter_todos(self) -> List[Equipamento]:
        return list(self._equipamentos.values())

    def remover(self, patrimonio: str) -> None:
        chave = self._normalizar(patrimonio)
        if chave not in self._equipamentos:
            raise PatrimonioNaoEncontradoError(chave)
        del self._equipamentos[chave]
        self._repositorio.salvar(self._equipamentos)

    def atualizar(
        self,
        patrimonio: str,
        tipo: Optional[TipoEquipamento] = None,
        marca: Optional[str] = None,
        modelo: Optional[str] = None,
        usuario: Optional[str] = None,
        setor: Optional[str] = None,
        status: Optional[StatusEquipamento] = None,
    ) -> Equipamento:
        """
        Edição parcial: só os campos informados (não-None) são
        alterados. O patrimônio em si é imutável — para "renomear" um
        patrimônio, o correto é remover e recadastrar, pois a chave de
        indexação é o próprio patrimônio.
        """
        chave = self._normalizar(patrimonio)
        atual = self._equipamentos.get(chave)
        if atual is None:
            raise PatrimonioNaoEncontradoError(chave)

        nova_marca = marca.strip() if marca is not None else atual.marca
        novo_modelo = modelo.strip() if modelo is not None else atual.modelo
        novo_usuario = usuario.strip() if usuario is not None else atual.usuario
        novo_setor = setor.strip() if setor is not None else atual.setor
        self._validar_campos_obrigatorios(nova_marca, novo_modelo, novo_usuario, novo_setor)

        atualizado = Equipamento(
            patrimonio=chave,
            tipo=tipo if tipo is not None else atual.tipo,
            marca=nova_marca,
            modelo=novo_modelo,
            usuario=novo_usuario,
            setor=novo_setor,
            status=status if status is not None else atual.status,
        )
        self._equipamentos[chave] = atualizado
        self._repositorio.salvar(self._equipamentos)
        return atualizado
