import streamlit as st
from view.home import home_view
from view.avaliacao_institucional import avaliacao_institucional_view
from view.avaliacao_das_disciplinas import avaliacao_das_disciplinas_view
from view.avaliacao_dos_cursos import avaliacao_dos_cursos_view
from services.HomeService import Authenticator

###### Lógica do Autenticador ######
VALID_USERNAME = "admin"
VALID_PASSWORD = "123" 
authenticator = Authenticator(VALID_USERNAME, VALID_PASSWORD)
def main():
    st.set_page_config(
        page_title="Dashboard UFPR",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    tabs = st.tabs([
        "Home",
        "Avaliação Institucional",
        "Avaliação de Disciplinas",
        "Avaliação dos Cursos"
    ])

    with tabs[0]:
        home_view()

    with tabs[1]:
        avaliacao_institucional_view()

    with tabs[2]:
        avaliacao_das_disciplinas_view()

    with tabs[3]:
        avaliacao_dos_cursos_view()
authenticator.secure_page(main)
