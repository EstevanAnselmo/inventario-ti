"""
Gate de login simples para uso interno.

Não é um sistema de autenticação completo (sem múltiplos usuários,
sem recuperação de senha) — é o suficiente para impedir acesso
casual a uma ferramenta interna pequena. As credenciais NUNCA ficam
no código: vêm de .streamlit/secrets.toml (que não deve ir pro
controle de versão) ou de variáveis de ambiente no servidor.

Evoluir para autenticação via Active Directory/LDAP (já que o
domínio da empresa existe) é o passo natural se o uso crescer.
"""

import hashlib
import streamlit as st


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def exigir_login() -> None:
    """
    Bloqueia o restante da página até o usuário informar usuário e
    senha corretos. Usa st.session_state para não pedir login de novo
    a cada interação (Streamlit reexecuta o script inteiro a cada clique).
    """
    if st.session_state.get("autenticado"):
        return

    st.title("Inventário de TI — Login")

    usuario_esperado = st.secrets.get("auth", {}).get("usuario")
    senha_hash_esperada = st.secrets.get("auth", {}).get("senha_sha256")

    if not usuario_esperado or not senha_hash_esperada:
        st.error(
            "Credenciais não configuradas. Defina [auth] usuario e senha_sha256 "
            "em .streamlit/secrets.toml antes de usar este app."
        )
        st.stop()

    with st.form("login_form"):
        usuario_digitado = st.text_input("Usuário")
        senha_digitada = st.text_input("Senha", type="password")
        enviado = st.form_submit_button("Entrar")

    if enviado:
        if usuario_digitado == usuario_esperado and _hash(senha_digitada) == senha_hash_esperada:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.stop()


def logout() -> None:
    st.session_state["autenticado"] = False
    st.rerun()
