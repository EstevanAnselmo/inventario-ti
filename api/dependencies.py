"""
Injeção de dependência da API.

O ponto central aqui: a *mesma* instância de InventarioService (e do
repositório por trás dela) é reaproveitada entre requisições via
lru_cache, em vez de recarregar o inventario.json inteiro a cada
requisição. Isso também é o único lugar do projeto que sabe qual
implementação concreta de repositório está em uso — trocar por
SQLite no futuro é uma mudança de uma linha, aqui.
"""

from functools import lru_cache

from repositories import JsonEquipamentoRepository
from services import InventarioService

CAMINHO_BANCO_DE_DADOS = "inventario.json"


@lru_cache
def obter_service() -> InventarioService:
    repositorio = JsonEquipamentoRepository(CAMINHO_BANCO_DE_DADOS)
    return InventarioService(repositorio)
