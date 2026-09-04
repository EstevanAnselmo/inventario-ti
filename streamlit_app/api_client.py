"""
Cliente HTTP para a API FastAPI do inventário.

Todo o app Streamlit fala com o backend só através deste módulo —
nenhuma outra parte do Streamlit monta URL ou chama requests
diretamente. Isso deixa a troca de endereço da API (local -> VPS)
restrita a um único lugar (API_BASE_URL).
"""

import requests
import streamlit as st

API_BASE_URL = st.secrets.get("api", {}).get("base_url", "http://127.0.0.1:8000")

TIMEOUT_SEGUNDOS = 10


def _tratar_resposta(resposta: requests.Response):
    """
    Padroniza o retorno de todas as chamadas: (sucesso, dados_ou_erro).
    Em caso de erro, tenta extrair a mensagem 'detail' que a API
    (FastAPI/HTTPException) já retorna nesse formato.
    """
    if resposta.status_code // 100 == 2:
        if resposta.status_code == 204 or not resposta.content:
            return True, None
        return True, resposta.json()

    try:
        detalhe = resposta.json().get("detail", resposta.text)
    except ValueError:
        detalhe = resposta.text
    return False, detalhe


def listar_equipamentos():
    try:
        resposta = requests.get(f"{API_BASE_URL}/equipamentos", timeout=TIMEOUT_SEGUNDOS)
    except requests.RequestException as erro:
        return False, f"Não foi possível conectar à API em {API_BASE_URL}: {erro}"
    return _tratar_resposta(resposta)


def buscar_equipamento(patrimonio: str):
    try:
        resposta = requests.get(
            f"{API_BASE_URL}/equipamentos/{patrimonio}", timeout=TIMEOUT_SEGUNDOS
        )
    except requests.RequestException as erro:
        return False, f"Não foi possível conectar à API em {API_BASE_URL}: {erro}"
    return _tratar_resposta(resposta)


def cadastrar_equipamento(payload: dict):
    try:
        resposta = requests.post(
            f"{API_BASE_URL}/equipamentos", json=payload, timeout=TIMEOUT_SEGUNDOS
        )
    except requests.RequestException as erro:
        return False, f"Não foi possível conectar à API em {API_BASE_URL}: {erro}"
    return _tratar_resposta(resposta)


def editar_equipamento(patrimonio: str, payload: dict):
    # Remove campos não preenchidos (None) para que o PATCH seja parcial de verdade
    payload_limpo = {chave: valor for chave, valor in payload.items() if valor not in (None, "")}
    try:
        resposta = requests.patch(
            f"{API_BASE_URL}/equipamentos/{patrimonio}",
            json=payload_limpo,
            timeout=TIMEOUT_SEGUNDOS,
        )
    except requests.RequestException as erro:
        return False, f"Não foi possível conectar à API em {API_BASE_URL}: {erro}"
    return _tratar_resposta(resposta)


def remover_equipamento(patrimonio: str):
    try:
        resposta = requests.delete(
            f"{API_BASE_URL}/equipamentos/{patrimonio}", timeout=TIMEOUT_SEGUNDOS
        )
    except requests.RequestException as erro:
        return False, f"Não foi possível conectar à API em {API_BASE_URL}: {erro}"
    return _tratar_resposta(resposta)
