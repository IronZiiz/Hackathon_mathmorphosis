import streamlit as st

def home_view():

    st.markdown(
        """
        <h1 style="text-align:center; font-size:2.4rem; font-weight:700;">
            Visualização dos Resultados da 
            <span style="color:#2563eb;">Avaliação</span> da UFPR
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            max-width:750px;
            margin:auto;
            font-size:1.1rem;
            color:#555;
        ">
            Ferramenta interativa desenvolvida pela Equipe Mathmorphosis para visualizar os resultados das pesquisas 
            realizadas junto a alunos e servidores da Universidade Federal do Paraná.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")  
    st.write("")  


    CARD_STYLE = """
    border:1px solid #ddd; 
    border-radius:12px; 
    padding:16px; 
    text-align:center;
    background-color:#fafafa;
    height:260px;               
    display:flex;
    flex-direction:column;
    justify-content:flex-start; 
"""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">📊</div>
                <h3 style="margin-top:10px;">Visualização Intuitiva</h3>
                <p>Gráficos e tabelas interativas para análise de frequências absolutas e relativas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">📚</div>
                <h3 style="margin-top:10px;">10 Dimensões Avaliativas</h3>
                <p>Análise completa seguindo os 5 eixos do SINAES com todas as dimensões de avaliação.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">🌎</div>
                <h3 style="margin-top:10px;">Acesso Público</h3>
                <p>Dados impessoais disponíveis para toda a comunidade acadêmica e sociedade.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.write("")  
    st.write("")  


    st.markdown(
        """
        <h1 style="text-align:center; font-size:2.4rem; font-weight:700;">
            Formato das Pesquisas
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            max-width:750px;
            margin:auto;
            font-size:1.1rem;
            color:#555;
        ">
            As pesquisas são compostas por questões apresentadas na forma de afirmações com três alternativas para o respondente.
        </p>
        """,
        unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">✅</div>
                <h3 style="margin-top:10px;">Concordo</h3>
                <p>Indica que o respondente concorda com a afirmação apresentada</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">❌</div>
                <h3 style="margin-top:10px;">Discordo</h3>
                <p>Indica que o respondente discorda da afirmação apresentada</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:2rem;">🔵</div>
                <h3 style="margin-top:10px;"></h3>
                <p>Indica que o respondente não tem conhecimento sobre o tema</p>
            </div>
            """,
            unsafe_allow_html=True,)