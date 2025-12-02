import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoDasDisciplinasService(DataLoader): 
    def __init__(self,
                df_load_dados_avaliacao_disciplinas_presencial = None,
                df_load_dados_avaliacao_disciplinas_EAD = None, 
                disciplina_value = None,
                curso_value = None,
                setor_value = None,
                dimensao_value = None,
                tipo_disciplina_value = None,
                 ):
        
        if df_load_dados_avaliacao_disciplinas_presencial is None:
            df_load_dados_avaliacao_disciplinas_presencial = DataLoader.load_dados_disciplinas_presencial()

        if df_load_dados_avaliacao_disciplinas_EAD is None: 
            df_load_dados_avaliacao_disciplinas_EAD = DataLoader.load_dados_disciplinas_EAD()
        
    
        self.df_presencial = df_load_dados_avaliacao_disciplinas_presencial
        self.df_EAD = df_load_dados_avaliacao_disciplinas_EAD
        self.disciplina_value = disciplina_value
        self.curso_value = curso_value 
        self.setor_value = setor_value
        self.dimensao_value = dimensao_value 
        self.tipo_disciplina_value = tipo_disciplina_value

    def df_disciplinas(self)-> pd.DataFrame: 
        if self.tipo_disciplina_value == 'Presencial': 
            df_disciplinas = self.df_presencial
        else: 
            df_disciplinas = self.df_EAD

        return df_disciplinas
    
    def _total_respostas_ano_atual(self): 
        df = self.df_disciplinas()
        df = df[['VALOR_RESPOSTA']]
        total_respostas = len(df)
        return total_respostas
    
    def get_total_respondentes_ano_atual(self) ->int: 
        df = self.df_disciplinas()
        return df["ID_PESQUISA"].nunique()

    def get_concordancia_atual(self) -> float:
        df = self.df_disciplinas()
        total = self._total_respostas_ano_atual()
        concordancia = len(df[df["VALOR_RESPOSTA"] == 1])
        return (concordancia / total ) * 100

    def get_discordancia_atual(self) -> float: 
        df = self.df_disciplinas()
        df = df[['VALOR_RESPOSTA']]
        total_respostas = self._total_respostas_ano_atual() 
        pct_insatisfacao_ano_atual = (df['VALOR_RESPOSTA'].eq(-1).sum() / total_respostas) * 100
        return pct_insatisfacao_ano_atual
    
    def get_desconhecimento(self) -> float: 
        df = self.df_disciplinas()
        total = self._total_respostas_ano_atual()
        discordancia = len(df[df["VALOR_RESPOSTA"] == 0])

        return (discordancia / total ) * 100
    
    def formatacao_disciplina_curso_setor(self) -> list:
        df = self.df_disciplinas().copy()

        # Remove espaços extras em todas as colunas relevantes
        for col in ["NOME_DISCIPLINA", "CURSO", "SETOR_CURSO"]:
            df[col] = df[col].astype(str).str.strip()

        df = df[['NOME_DISCIPLINA','CURSO','SETOR_CURSO']].drop_duplicates()

        opcoes = [
            f"Disciplina:{row.NOME_DISCIPLINA} - Curso: {row.CURSO} - Setor: {row.SETOR_CURSO}"
            for row in df.itertuples()
        ]

        return ["Todas as disciplinas"] + sorted(opcoes)
    
    def df_filtrado_pela_disciplina_curso_setor(self) -> pd.DataFrame:
        df = self.df_disciplinas().copy()

        for col in ["NOME_DISCIPLINA", "CURSO", "SETOR_CURSO"]:
            df[col] = df[col].astype(str).str.strip()

        filtros = {
            "NOME_DISCIPLINA": self.disciplina_value,
            "CURSO": self.curso_value,
            "SETOR_CURSO": self.setor_value,
        }

        for coluna, valor in filtros.items():
            if self.disciplina_value != "Todas":
                df = df[df[coluna] == valor]

        return df
    
    def grafico_distribuicao_total_donut(self):
        disciplina_value = self.disciplina_value
        curso_value = self.curso_value 
        setor_value =self.setor_value
         

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.df_filtrado_pela_disciplina_curso_setor()
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
        if curso_value =='Todas': 
            fig_donut.update_layout(
            
                title=f"Distribuição Geral de Respostas: {curso_value}",
                showlegend=False,
                margin=dict(t=40, b=0, l=0, r=0),
                height=400
            )
        else:
            fig_donut.update_layout(
            
                title={
                    'text': f"Distribuição Geral de Respostas",
                },
                showlegend=False,
                margin=dict(t=100, b=0, l=0, r=0),
                height=400)


        return total_resp, fig_donut
        
    def grafico_resumo_por_eixo(self):
        COLOR_MAP = {
        'Concordo': '#2ecc71',
        'Discordo': '#e74c3c',
        'Desconheço': '#95a5a6'
        }
        
        df_filtered = self.df_filtrado_pela_disciplina_curso_setor()

        if df_filtered.empty:
            return None
        
        df_filtered['EIXO_NOME'] = df_filtered['EIXO_NOME'].fillna(
            df_filtered['EIXO_NOME'].str.replace("_", " ").str.title()
        )

        df_grouped = (
            df_filtered.groupby(['EIXO_NOME', 'RESPOSTA'])
            .size()
            .reset_index(name='COUNT')
        )

        total_por_eixo = (
            df_filtered.groupby('EIXO_NOME')
            .size()
            .reset_index(name='TOTAL')
        )

        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO_NOME')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        df_merged = df_merged.sort_values('EIXO_NOME')

        df_merged["LABEL"] = df_merged.apply(
            lambda row: f"{row['PERCENT']:.1f}% ({row['COUNT']})", axis=1
        )

        fig_bar = px.bar(
            df_merged,
            x='EIXO_NOME',
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
