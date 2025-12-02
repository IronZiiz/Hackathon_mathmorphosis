import streamlit as st
from services.LoginService import LoginService

import time

def login_view():
    col1, col2, col3 = st.columns(3)

    container = col2.empty()

    if not st.session_state.get("authenticated", False):

        with container.container():
            st.subheader("Login Necessário")

            with st.form("login_form"):
                user_input = st.text_input("Nome de Usuário")
                pass_input = st.text_input("Senha", type="password")
                submitted = st.form_submit_button("Entrar")

        if submitted:
            login_service = LoginService(
                username=user_input,
                password=pass_input
            )

            result = login_service.authenticate()

            if result["success"]:
                container.success(result["message"])
                time.sleep(1.5)

                st.session_state["authenticated"] = True
                st.rerun()
            else:
                container.error(result["message"])

    else:
        with container.container():
            with col1: 
                file1 = st.file_uploader("Arquivo Avaliação Institucional", type=["csv", "xlsx"])
            with col2: 
                file2 = st.file_uploader("Arquivo Avaliação Cursos", type=["csv", "xlsx" ])
            with col3:
                file3 = st.file_uploader("Arquivo Avaliação Disciplinas", type=["csv", "xlsx"])

            return file1, file2, file3

