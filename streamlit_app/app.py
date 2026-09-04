"""
Interface Streamlit do Inventário de TI.

Roda com:
    streamlit run app.py
(a partir da pasta streamlit_app/, com a API já rodando)

Este arquivo só cuida de layout e navegação. Toda comunicação com o
backend passa por api_client.py — nenhuma regra de negócio mora aqui.
"""

import pandas as pd
import streamlit as st

import api_client
from auth import exigir_login, logout

TIPOS = ["Notebook", "Desktop", "Tablet", "Monitor", "Impressora", "Outro"]
STATUS = ["Ativo", "Em Manutenção", "Baixado", "Em Estoque"]

st.set_page_config(page_title="Inventário de TI", page_icon="🖥️", layout="wide")

exigir_login()

with st.sidebar:
    st.title("🖥️ Inventário de TI")
    pagina = st.radio(
        "Navegação",
        ["Listar / Exportar", "Cadastrar", "Editar", "Remover"],
    )
    st.divider()
    if st.button("Sair"):
        logout()


def _equipamentos_para_dataframe(equipamentos: list) -> pd.DataFrame:
    if not equipamentos:
        return pd.DataFrame(
            columns=["patrimonio", "tipo", "marca", "modelo", "usuario", "setor", "status"]
        )
    return pd.DataFrame(equipamentos)


# ---------------------------------------------------------------
# TELA: Listar / Exportar
# ---------------------------------------------------------------
if pagina == "Listar / Exportar":
    st.header("Equipamentos cadastrados")

    ok, resultado = api_client.listar_equipamentos()
    if not ok:
        st.error(f"Erro ao carregar equipamentos: {resultado}")
    else:
        df = _equipamentos_para_dataframe(resultado)
        st.dataframe(df, use_container_width=True, hide_index=True)

        if not df.empty:
            csv = df.to_csv(index=False).encode("utf-8-sig")  # utf-8-sig abre certo no Excel
            st.download_button(
                "⬇️ Exportar para CSV",
                data=csv,
                file_name="inventario_ti.csv",
                mime="text/csv",
            )
        else:
            st.info("Nenhum equipamento cadastrado ainda.")

# ---------------------------------------------------------------
# TELA: Cadastrar
# ---------------------------------------------------------------
elif pagina == "Cadastrar":
    st.header("Cadastrar equipamento")

    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            patrimonio = st.text_input("Patrimônio *")
            tipo = st.selectbox("Tipo *", TIPOS)
            marca = st.text_input("Marca *")
            modelo = st.text_input("Modelo *")
        with col2:
            usuario = st.text_input("Usuário *")
            setor = st.text_input("Setor *")
            status = st.selectbox("Status", STATUS, index=0)

        enviado = st.form_submit_button("Cadastrar")

    if enviado:
        payload = {
            "patrimonio": patrimonio,
            "tipo": tipo,
            "marca": marca,
            "modelo": modelo,
            "usuario": usuario,
            "setor": setor,
            "status": status,
        }
        ok, resultado = api_client.cadastrar_equipamento(payload)
        if ok:
            st.success(f"Equipamento '{resultado['patrimonio']}' cadastrado com sucesso.")
        else:
            st.error(f"Erro ao cadastrar: {resultado}")

# ---------------------------------------------------------------
# TELA: Editar
# ---------------------------------------------------------------
elif pagina == "Editar":
    st.header("Editar equipamento")

    patrimonio_busca = st.text_input("Digite o patrimônio para buscar")

    if patrimonio_busca:
        ok, equipamento = api_client.buscar_equipamento(patrimonio_busca)
        if not ok:
            st.warning(f"{equipamento}")
        else:
            st.write("Deixe em branco os campos que não quer alterar.")
            with st.form("form_edicao"):
                col1, col2 = st.columns(2)
                with col1:
                    tipo = st.selectbox(
                        "Tipo", [""] + TIPOS, index=0,
                        help=f"Atual: {equipamento['tipo']}",
                    )
                    marca = st.text_input("Marca", placeholder=equipamento["marca"])
                    modelo = st.text_input("Modelo", placeholder=equipamento["modelo"])
                with col2:
                    usuario = st.text_input("Usuário", placeholder=equipamento["usuario"])
                    setor = st.text_input("Setor", placeholder=equipamento["setor"])
                    status = st.selectbox(
                        "Status", [""] + STATUS, index=0,
                        help=f"Atual: {equipamento['status']}",
                    )

                enviado = st.form_submit_button("Salvar alterações")

            if enviado:
                payload = {
                    "tipo": tipo or None,
                    "marca": marca or None,
                    "modelo": modelo or None,
                    "usuario": usuario or None,
                    "setor": setor or None,
                    "status": status or None,
                }
                ok, resultado = api_client.editar_equipamento(patrimonio_busca, payload)
                if ok:
                    st.success("Equipamento atualizado com sucesso.")
                    st.json(resultado)
                else:
                    st.error(f"Erro ao editar: {resultado}")

# ---------------------------------------------------------------
# TELA: Remover
# ---------------------------------------------------------------
elif pagina == "Remover":
    st.header("Remover equipamento")

    patrimonio_remover = st.text_input("Digite o patrimônio a remover")
    confirmar = st.checkbox("Confirmo que quero remover este equipamento")

    if st.button("Remover", type="primary", disabled=not confirmar):
        ok, resultado = api_client.remover_equipamento(patrimonio_remover)
        if ok:
            st.success(f"Patrimônio '{patrimonio_remover}' removido com sucesso.")
        else:
            st.error(f"Erro ao remover: {resultado}")
