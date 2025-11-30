import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoInstitucionalService(DataLoader): 
    def __init__(
        self, 
        eixos_value=None,
        perguntas_value=None,
        df_load_dados_institucional=None,
    ):
        if df_load_dados_institucional is None:
            df_load_dados_institucional = DataLoader.load_dados_institucional()

        self.df_load_dados_institucional = df_load_dados_institucional
        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value

    def filtrar_dados_institucionais(self):
        df = self.df_load_dados_institucional.copy()

        eixo_value = self.eixos_value
        pergunta_value = self.perguntas_value

        if isinstance(eixo_value, str):
            eixo_value = [eixo_value]
        if isinstance(pergunta_value, str):
            pergunta_value = [pergunta_value]

        if not eixo_value or "Todos" in eixo_value:
            df_filtered = df.copy()
        else:
            df_filtered = df[df["EIXO"].isin(eixo_value)].sort_values(by="Ordem")

        if pergunta_value and "Todos" not in pergunta_value:
            perguntas_extraidas = [p.split(" - ", 1)[1] for p in pergunta_value]
            df_filtered = df_filtered[df_filtered["PERGUNTA"].isin(perguntas_extraidas)]

        
        return df_filtered


    
    def total_respondentes_ano_atual(self): 
        df = self.df_load_dados_institucional
        qtd_respondentes_atual = df['ID_PESQUISA'].nunique()
        return qtd_respondentes_atual
    
    def total_respondentes_ano_passado(self): 
        qtd_respondentes_ano_atual = self.total_respondentes_ano_atual()
        qtd_respondentes_ano_passado = 50
        pct_comparacao_ano_atual =(qtd_respondentes_ano_atual/qtd_respondentes_ano_passado - 1)*100
        return pct_comparacao_ano_atual,qtd_respondentes_ano_passado
    
    # satisfação = concordancia pois frases afirmativas positivas
    def total_respostas_ano_atual(self): 
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = len(df)
        return total_respostas

    def satisfacao_ano_atual(self):
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        
        pct_satisfacao_ano_atual = (df['RESPOSTA'].eq('Concordo').sum() / total_respostas) * 100

        return pct_satisfacao_ano_atual
    
    def satisfacao_ano_passado(self):
            pct_satisfacao_ano_passado = 10
            return pct_satisfacao_ano_passado
    
    def insatisfacao_ano_atual(self):
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        pct_insatisfacao_ano_atual = (df['RESPOSTA'].eq('Discordo').sum() / total_respostas) * 100
        return pct_insatisfacao_ano_atual
    
    def insatisfacao_ano_passado(self):
        pct_insatisfacao_ano_passado = 10
        return pct_insatisfacao_ano_passado 
    
    def desconhecimento_ano_atual(self): 
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        pct_desconhecimento_ano_atual = (df['RESPOSTA'].eq('Desconheço').sum() / total_respostas) * 100
        return pct_desconhecimento_ano_atual
    
    def desconhecimento_ano_passado(self): 
        pct_desconhecimento_ano_passado = 10 
        return pct_desconhecimento_ano_passado 

    def grafico_distribuicao_total_donut(self):

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.filtrar_dados_institucionais()
        total_resp = len(df_filtered)

        if total_resp == 0:
            return None

        df_pizza = df_filtered["RESPOSTA"].value_counts().reset_index()
        df_pizza.columns = ["RESPOSTA", "CONTAGEM"]

        fig_donut = px.pie(
            df_pizza,
            values='CONTAGEM',
            names='RESPOSTA',
            hole=0.5,
            color='RESPOSTA',
            color_discrete_map=COLOR_MAP
        )

        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label'
            
        )

        fig_donut.update_layout(
            title="Distribuição Geral de Respostas",
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            height=400
        )

        return total_resp, fig_donut

    def grafico_resumo_por_eixo(self):
        COLOR_MAP = {
        'Concordo': '#2ecc71',
        'Discordo': '#e74c3c',
        'Desconheço': '#95a5a6'
        }
        df_filtered = self.filtrar_dados_institucionais()
        if df_filtered.empty:
            return None

        df_grouped = (
            df_filtered.groupby(['EIXO', 'RESPOSTA'])
            .size()
            .reset_index(name='COUNT')
        )

        total_por_eixo = (
            df_filtered.groupby('EIXO')
            .size()
            .reset_index(name='TOTAL')
        )

        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        df_merged = df_merged.sort_values('EIXO')

        df_merged["LABEL"] = df_merged.apply(
            lambda row: f"{row['PERCENT']:.1f}% ({row['COUNT']})", axis=1
        )

        fig_bar = px.bar(
            df_merged,
            x="EIXO",
            y="PERCENT",
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP,
            barmode='stack',
            text="LABEL",
            height=500
        )

        fig_bar.update_traces(
            textposition="inside",
            insidetextanchor="middle"
        )

        fig_bar.update_layout(
            title = 'Distribuição de respostas por eixos',
            xaxis_title="Eixo",
            yaxis_title="% das Respostas",
            legend_title="",
            margin=dict(l=10, r=10, t=45, b=0),
            yaxis=dict(range=[0, 100]),
            xaxis=dict(tickangle=10)
        )

        return fig_bar

    
    def grafico_dist_por_eixo_barra(self): 
        fig = 'grafico'
        dataframe_fig = 'Data frame usado para construir a fig'
        return fig, dataframe_fig
    
    def grafico_perguntas(self): 
        fig = 'grafico'
        dataframe_fig = 'Data frame usado para construir a fig'
        return fig, dataframe_fig
    
    def df_dados_brutos(self):
        dados_brutos = 'Dados com valores de freq relativa e absoluta'
        return dados_brutos
    
    def preparar_dados_unidade_gestora(self):
        df = self.df_load_dados_institucional[['ID_PESQUISA', 'UNIDADE GESTORA']]
        df = df.dropna(subset=['UNIDADE GESTORA'])

        dataframe_fig = (
            df.groupby('UNIDADE GESTORA')
            .size()
            .reset_index(name='TOTAL_RESPOSTAS')
            .sort_values('TOTAL_RESPOSTAS', ascending=True)
        )

        return dataframe_fig

    
    def grafico_barra_unidade_gestora(self):
        dataframe_fig = self.preparar_dados_unidade_gestora()
        dataframe_fig = dataframe_fig.nlargest(10, 'TOTAL_RESPOSTAS')
        dataframe_fig = dataframe_fig.sort_values('TOTAL_RESPOSTAS', ascending=True)


        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=dataframe_fig['UNIDADE GESTORA'],
            x=dataframe_fig['TOTAL_RESPOSTAS'],
            orientation='h',
            marker_color='#3498db',
            text=dataframe_fig['TOTAL_RESPOSTAS'],
            textposition='auto'
        ))

        fig_bar.update_layout(
            title="Top 10 Unidades número de respostas nas pesquisas",
            xaxis_title="Total de Respostas",
            yaxis_title="Unidade Gestora",
            height=500,
            bargap=0.15
        )
        return fig_bar
    
    def grafico_donut_top10(self):
        df = self.df_load_dados_institucional[['ID_PESQUISA', 'UNIDADE GESTORA']].dropna()
        df_unique = df.drop_duplicates(subset=['ID_PESQUISA'])

        total_geral = df_unique['ID_PESQUISA'].nunique()

        df_contagem = (
            df_unique.groupby('UNIDADE GESTORA')['ID_PESQUISA']
            .count()
            .reset_index(name='TOTAL_PESSOAS')
        )

        df_top10 = df_contagem.nlargest(10, 'TOTAL_PESSOAS')
        total_top10 = df_top10['TOTAL_PESSOAS'].sum()

        total_outras = total_geral - total_top10

        labels = ["Top 10 Unidades Gestoras", "Outras Unidades Gestoras"]
        values = [total_top10, total_outras]

        fig_donut = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                textinfo="label+percent+value",
                marker=dict(colors=["#3498db", "#95a5a6"])
            )
        ])

        fig_donut.update_layout(
            showlegend=False,
            title="Participação do TOP 10 no Total de Respondentes",
            height=500
        )

        return fig_donut


    
    