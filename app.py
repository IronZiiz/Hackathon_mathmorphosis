import streamlit as st
from view.home import home_view
from view.avaliacao_institucional import avaliacao_institucional_view
from view.avaliacao_das_disciplinas import avaliacao_das_disciplinas_view
from view.avaliacao_dos_cursos import avaliacao_dos_cursos_view

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
