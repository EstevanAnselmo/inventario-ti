"""
Modelo de dados do equipamento.

Usa Enums para 'status' e 'tipo' em vez de string livre: isso torna
impossível, a nível de tipo, cadastrar "Ativo", "ativo" e "ATIVO"
como três valores diferentes — problema comum em sistemas que usam
string livre para campos de domínio fechado.
"""

from dataclasses import dataclass, asdict
from enum import Enum

from exceptions import DadosInvalidosError


class StatusEquipamento(str, Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Em Manutenção"
    BAIXADO = "Baixado"
    ESTOQUE = "Em Estoque"


class TipoEquipamento(str, Enum):
    NOTEBOOK = "Notebook"
    DESKTOP = "Desktop"
    TABLET = "Tablet"
    MONITOR = "Monitor"
    IMPRESSORA = "Impressora"
    OUTRO = "Outro"


@dataclass
class Equipamento:
    patrimonio: str
    tipo: TipoEquipamento
    marca: str
    modelo: str
    usuario: str
    setor: str
    status: StatusEquipamento = StatusEquipamento.ATIVO

    def to_dict(self) -> dict:
        """Serializa para dict com Enums convertidos em string (JSON-safe)."""
        dados = asdict(self)
        dados["tipo"] = self.tipo.value
        dados["status"] = self.status.value
        return dados

    @staticmethod
    def from_dict(dados: dict) -> "Equipamento":
        """
        Reconstrói o objeto a partir de um dict (tipicamente vindo do
        JSON), validando os campos obrigatórios e convertendo os
        valores de Enum. Lança DadosInvalidosError se o schema estiver
        incorreto — chave ausente ou valor de enum desconhecido —
        para que a camada de repositório trate isso como falha de
        persistência, e não deixe um objeto inconsistente entrar em
        memória silenciosamente.
        """
        try:
            return Equipamento(
                patrimonio=dados["patrimonio"],
                tipo=TipoEquipamento(dados["tipo"]),
                marca=dados["marca"],
                modelo=dados["modelo"],
                usuario=dados["usuario"],
                setor=dados["setor"],
                status=StatusEquipamento(dados.get("status", StatusEquipamento.ATIVO.value)),
            )
        except KeyError as erro:
            raise DadosInvalidosError(f"Campo obrigatório ausente no registro: {erro}") from erro
        except ValueError as erro:
            raise DadosInvalidosError(f"Valor inválido no registro: {erro}") from erro
