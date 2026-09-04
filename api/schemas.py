"""
Schemas Pydantic — o "contrato" público da API.

Propositalmente separados do models/equipamento.py (que é a entidade
de domínio). Misturar os dois é uma armadilha comum: qualquer mudança
interna no dataclass acabaria vazando pro contrato HTTP, e vice-versa.
Aqui a conversão entre um e outro é explícita (equipamento_para_response).
"""

from pydantic import BaseModel, Field

from models import StatusEquipamento, TipoEquipamento


class EquipamentoCreate(BaseModel):
    patrimonio: str = Field(..., min_length=1, examples=["PT-001"])
    tipo: TipoEquipamento
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    usuario: str = Field(..., min_length=1)
    setor: str = Field(..., min_length=1)
    status: StatusEquipamento = StatusEquipamento.ATIVO


class EquipamentoUpdate(BaseModel):
    """Todos os campos são opcionais: só o que vier preenchido é alterado (PATCH)."""

    tipo: TipoEquipamento | None = None
    marca: str | None = Field(default=None, min_length=1)
    modelo: str | None = Field(default=None, min_length=1)
    usuario: str | None = Field(default=None, min_length=1)
    setor: str | None = Field(default=None, min_length=1)
    status: StatusEquipamento | None = None


class EquipamentoResponse(BaseModel):
    patrimonio: str
    tipo: TipoEquipamento
    marca: str
    modelo: str
    usuario: str
    setor: str
    status: StatusEquipamento


class ErroResponse(BaseModel):
    detalhe: str
