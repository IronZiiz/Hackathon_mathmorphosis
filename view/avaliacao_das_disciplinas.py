import streamlit as st 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from services.AvaliacaoDasDisciplinasService import AvaliacaoDasDisciplinasService
 
BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}

def avaliacao_das_disciplinas_view():
    
    
    st.title('Resultados Avaliação Disciplinas')

    col1,col2,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano/Período', 
                                ('2025/2','2025/1','2024/2', '2024/1'),
                                index = 0, key = "year_value_disciplina")
    with col2: 
        tipo_disciplina_value = st.selectbox('Presencial/EAD', 
                                             ('Presencial','EAD'), 
                                             index = 0, key = "tipo_disciplina_value"
                                             )
        tipo_disciplina_value = str(tipo_disciplina_value)

    service = AvaliacaoDasDisciplinasService(
        tipo_disciplina_value=tipo_disciplina_value)

    col1,col2,col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=service.get_total_respondentes_ano_atual(),
            delta=f"% Ano passado: "
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.get_concordancia_atual():.2f}%",
            delta=1,
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.get_discordancia_atual():.2f}%",
            delta=2,
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.get_desconhecimento():.2f}%",
            delta=1
        )
    
    select_box_value_disciplina_curso_setor = st.selectbox("Pesquise a disciplina de seu interesse",
                                   service.formatacao_disciplina_curso_setor())
    
    select_box_value_disciplina_curso_setor = str(select_box_value_disciplina_curso_setor)
    if select_box_value_disciplina_curso_setor == "Todas as disciplinas":
        disciplina_value = "Todas"
        curso_value = "Todas"
        setor_value = "Todas"
    else:
        partes = select_box_value_disciplina_curso_setor.split(" - ")
        disciplina_value = partes[0].replace("Disciplina:", "").strip()
        curso_value = partes[1].replace("Curso:", "").strip()
        setor_value = partes[2].replace("Setor:", "").strip()
        
    service = AvaliacaoDasDisciplinasService(
        tipo_disciplina_value=tipo_disciplina_value,
        disciplina_value= disciplina_value,
        curso_value= curso_value,
        setor_value= setor_value)

    df_disciplina = pd.DataFrame({
    "RESPOSTA": ["Concordo", "Discordo", "Desconheço"],
    "CONTAGEM": [40, 10, 8]
    })

    df_setor = pd.DataFrame({
        "RESPOSTA": ["Concordo", "Discordo", "Desconheço"],
        "CONTAGEM": [70, 20, 15]
    })

    df_curso = pd.DataFrame({
        "RESPOSTA": ["Concordo", "Discordo", "Desconheço"],
        "CONTAGEM": [55, 12, 5]
    })
    col1, col2 = st.columns(2)
    with col1:
        _, fig_donut = service.grafico_distribuicao_total_donut()

        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.plotly_chart(service.grafico_resumo_por_eixo(), use_container_width=True)

    dimensoes = ["Dimensão 1", "Dimensão 2"]
    dim_sel = st.selectbox(
        "Selecione a Dimensão para Análise Detalhada:",
        dimensoes
    )

    questions = [
        "A disciplina apresenta boa organização geral",
        "Os materiais utilizados são adequados",
        "A infraestrutura atende às necessidades",
        "O docente promove participação dos estudantes"
    ]

    concordo_list = [70, 55, 62, 80]
    discordo_list = [15, 30, 20, 10]
    discordo_neg_list = [-x for x in discordo_list]

    def quebrar_texto(texto, max_chars=50):
        if len(texto) <= max_chars:
            return texto
        palavras = texto.split()
        linhas = []
        linha = ""
        for p in palavras:
            if len(linha) + len(p) + 1 <= max_chars:
                linha += p + " "
            else:
                linhas.append(linha.strip())
                linha = p + " "
        if linha:
            linhas.append(linha.strip())
        return "<br>".join(linhas)

    questions_formatted = [quebrar_texto(q) for q in questions]

    fig_div = go.Figure()

    fig_div.add_trace(go.Bar(
        y=questions_formatted,
        x=discordo_neg_list,
        name='Discordo',
        orientation='h',
        marker_color='#e74c3c',
        text=[f"{x:.1f}%" for x in discordo_list],
        textposition='auto',
        hoverinfo='text+y',
        hovertext=[f"Discordância: {x:.1f}%" for x in discordo_list]
    ))

    fig_div.add_trace(go.Bar(
        y=questions_formatted,
        x=concordo_list,
        name='Concordo',
        orientation='h',
        marker_color='#2ecc71',
        text=[f"{x:.1f}%" for x in concordo_list],
        textposition='auto',
        hoverinfo='text+y',
        hovertext=[f"Concordância: {x:.1f}%" for x in concordo_list]
    ))

    fig_div.update_layout(
        barmode='relative',
        title=f"Saldo de Opinião por Questão: {dim_sel}",
        xaxis_title="% Rejeição <---> % Aprovação",
        yaxis=dict(title=""),
        bargap=0.3,
        legend_title_text='Sentimento',
        height=len(questions) * 60 + 200
    )

    fig_div.add_vline(x=0, line_width=1, line_color="black")

    st.plotly_chart(fig_div, use_container_width=True)

    st.header("Comparação com o Setor e Curso")
    col1, col2 = st.columns(2)
    with col1:
        
        _, fig_donut_setor = service.grafico_donut_setor()        
        st.plotly_chart(fig_donut_setor, use_container_width=True)

    with col2:
        _, fig_donut_curso = service.grafico_donut_curso()

        fig = px.pie(
            df_curso,
            values="CONTAGEM",
            names="RESPOSTA",
            hole=0.5,
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_donut_curso, use_container_width=True)

   

    st.header("Distribuição Geral do Sentimento Médio")

    st.plotly_chart(service.grafico_distribuicao_geral_sentimento(), use_container_width=True)

    st.markdown("""
    **Insight:** A grande maioria dos respondentes tem sentimento médio entre **0 e +1**, 
    mostrando que o padrão geral é positivo.
    """)

    st.markdown("---")
    with st.expander("Ver dados brutos (Frequências Absolutas) (TEMPORÁRIO0"):
        st.dataframe()
        st.download_button('Download Dados brutos',data="aa")

    