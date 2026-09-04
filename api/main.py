"""
Ponto de entrada da API.

Rodar com:
    uvicorn api.main:app --reload
a partir da raiz do projeto (inventario_ti/).

Documentação interativa gerada automaticamente em /docs (Swagger)
e /redoc.
"""

from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Inventário de TI",
    description="API para cadastro, consulta, edição e remoção de equipamentos de TI.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", tags=["infra"])
def health_check() -> dict:
    """Endpoint simples de verificação de disponibilidade (para monitoramento)."""
    return {"status": "ok"}
