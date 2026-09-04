"""
Exceções de domínio do sistema de inventário.

Separadas em um módulo próprio para evitar import circular entre
services/ e repositories/ (ambos precisam lançá-las) e para deixar
explícito quais erros pertencem ao domínio do negócio, em vez de
vazar exceções técnicas genéricas (OSError, json.JSONDecodeError
etc.) diretamente para a camada de interface.
"""


class InventarioError(Exception):
    """Classe base para todos os erros do domínio de inventário."""


class PatrimonioDuplicadoError(InventarioError):
    """Lançada ao tentar cadastrar um patrimônio já existente."""

    def __init__(self, patrimonio: str):
        self.patrimonio = patrimonio
        super().__init__(f"Patrimônio '{patrimonio}' já cadastrado.")


class PatrimonioNaoEncontradoError(InventarioError):
    """Lançada ao buscar, remover ou editar um patrimônio inexistente."""

    def __init__(self, patrimonio: str):
        self.patrimonio = patrimonio
        super().__init__(f"Patrimônio '{patrimonio}' não encontrado.")


class DadosInvalidosError(InventarioError):
    """
    Lançada quando um campo obrigatório está vazio, um valor de Enum é
    desconhecido, ou um registro carregado do armazenamento não segue
    o schema esperado (chave ausente, tipo incorreto etc.).
    """

    def __init__(self, motivo: str):
        super().__init__(motivo)


class PersistenciaError(InventarioError):
    """
    Lançada para qualquer falha ao ler ou gravar o armazenamento
    (arquivo corrompido, JSON inválido, erro de I/O, permissão negada).
    Isola a camada de serviço dos detalhes técnicos do mecanismo de
    persistência usado hoje (JSON em arquivo) — se um dia trocar para
    SQLite, essa é a única camada que muda.
    """
