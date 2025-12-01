from services.DataLoader  import DataLoader
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import json

class DataLogger:
    @staticmethod
    def save_feedback_to_json(data):
        filename = "feedback_log.json"
        if data == 1:
            _data = {"feedback": "Ótimo"}
        elif data == 0:
            _data = {"feedback": "Ruim"}
        try:
            with open(filename, 'a+', encoding='utf-8') as f:
                json_record = json.dumps(_data, ensure_ascii=False)
                f.write(json_record + '\n') 
            st.success(f"Feedback salvo em {filename}")
        except Exception as e:
            st.error(f"Erro ao salvar feedback: {e}")

import streamlit as st

class Authenticator:
    """
    Gerencia a autenticação de usuários com um nome de usuário e senha predefinidos.
    Utiliza st.session_state para manter o estado do login.
    """
    def __init__(self, username, password):
        """
        Inicializa o autenticador com credenciais fixas.
        Em um ambiente real, estas viriam de um banco de dados ou arquivo de configuração.
        """
        self.username = username
        self.password = password
        
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'user' not in st.session_state:
            st.session_state['user'] = None

    def display_login_form(self):
        """
        Exibe o formulário de login (username e password) e processa a submissão.
        """
        with st.container():
            st.subheader("Login Necessário")

            with st.form("login_form"):
                user_input = st.text_input("Nome de Usuário")
                pass_input = st.text_input("Senha", type="password")
                
                submitted = st.form_submit_button("Entrar")

                if submitted:
                    if user_input == self.username and pass_input == self.password:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user_input
                        st.success(f"Bem-vindo(a), {user_input}!")
                        st.rerun() 
                    else:
                        st.error("Nome de usuário ou senha incorretos.")

    def check_login_status(self):
        """
        Retorna True se o usuário estiver autenticado, False caso contrário.
        """
        return st.session_state.get('authenticated', False)

    def display_logout_button(self):
        """
        Exibe o botão de Logout e processa a saída.
        """
        if self.check_login_status():
            if st.sidebar.button("Logout"):
                st.session_state['authenticated'] = False
                st.session_state['user'] = None
                st.success("Sessão encerrada.")
                st.rerun()

    def secure_page(self, main_content_function):
        """
        Controla o acesso à página: se não estiver logado, mostra o formulário; 
        se estiver logado, executa a função de conteúdo principal.
        """
        self.display_logout_button() 

        if self.check_login_status():
            main_content_function()
        else:
            self.display_login_form()
