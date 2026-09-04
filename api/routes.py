"""
Rotas HTTP do inventário.

Cada endpoint faz três coisas, nessa ordem, e nada além disso:
  1. recebe/valida a entrada (o Pydantic já validou o schema antes
     de a função ser chamada);
  2. chama o InventarioService;
  3. traduz o resultado (ou a exceção de domínio) para HTTP.

Nenhuma regra de negócio mora aqui — se você notar uma condição de
negócio dentro de uma rota, ela deveria estar em services/.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models import Equipamento
from services import InventarioService
from exceptions import (
    PatrimonioDuplicadoError,
    PatrimonioNaoEncontradoError,
    DadosInvalidosError,
    PersistenciaError,
)
from api.schemas import EquipamentoCreate, EquipamentoUpdate, EquipamentoResponse
from api.dependencies import obter_service

router = APIRouter(prefix="/equipamentos", tags=["equipamentos"])


def _para_response(equipamento: Equipamento) -> EquipamentoResponse:
    return EquipamentoResponse(**equipamento.to_dict())


@router.post(
    "",
    response_model=EquipamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar(
    dados: EquipamentoCreate,
    service: InventarioService = Depends(obter_service),
) -> EquipamentoResponse:
    try:
        equipamento = service.adicionar(
            patrimonio=dados.patrimonio,
            tipo=dados.tipo,
            marca=dados.marca,
            modelo=dados.modelo,
            usuario=dados.usuario,
            setor=dados.setor,
            status=dados.status,
        )
    except PatrimonioDuplicadoError as erro:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(erro)) from erro
    except DadosInvalidosError as erro:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)) from erro
    return _para_response(equipamento)


@router.get("", response_model=List[EquipamentoResponse])
def listar(service: InventarioService = Depends(obter_service)) -> List[EquipamentoResponse]:
    return [_para_response(eq) for eq in service.obter_todos()]


@router.get("/{patrimonio}", response_model=EquipamentoResponse)
def buscar(
    patrimonio: str,
    service: InventarioService = Depends(obter_service),
) -> EquipamentoResponse:
    equipamento = service.buscar(patrimonio)
    if equipamento is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Patrimônio '{patrimonio}' não encontrado."
        )
    return _para_response(equipamento)


@router.patch("/{patrimonio}", response_model=EquipamentoResponse)
def editar(
    patrimonio: str,
    dados: EquipamentoUpdate,
    service: InventarioService = Depends(obter_service),
) -> EquipamentoResponse:
    try:
        equipamento = service.atualizar(
            patrimonio=patrimonio,
            tipo=dados.tipo,
            marca=dados.marca,
            modelo=dados.modelo,
            usuario=dados.usuario,
            setor=dados.setor,
            status=dados.status,
        )
    except PatrimonioNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
    except DadosInvalidosError as erro:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)) from erro
    return _para_response(equipamento)


@router.delete("/{patrimonio}", status_code=status.HTTP_204_NO_CONTENT)
def remover(
    patrimonio: str,
    service: InventarioService = Depends(obter_service),
) -> None:
    try:
        service.remover(patrimonio)
    except PatrimonioNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)) from erro
