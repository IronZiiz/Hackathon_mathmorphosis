from services.DataLoader  import DataLoader
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import textwrap

class AvaliacaoDosCursosService(DataLoader):
    """Serviço para análise das avaliações por curso.

    Fornece métodos para calcular métricas de respondentes e respostas,
    além de gerar gráficos de distribuição e radar por dimensão.
    """
    def __init__(self,
                df_load_dados_curso = None,
                curso_value = None,
                setor_value = None,
                dimensao_value = None, 
                ):
        """Inicializa o serviço com DataFrame opcional e filtros.

        Parâmetros
        ----------
        df_load_dados_curso : pd.DataFrame | None
            DataFrame com os dados do curso; carregado via DataLoader se None.
        curso_value, setor_value, dimensao_value : opcionais
            Valores usados para filtrar os dados nas visualizações.
        """
        if df_load_dados_curso is None:
            df_load_dados_curso = DataLoader.load_dados_curso()

        self.df = df_load_dados_curso
        self.curso_value = curso_value
        self.dimensao_value = dimensao_value

    def get_total_respondentes(self) -> int:
        """Retorna o número de respondentes únicos (ID_PESQUISA)."""
        return self.df["ID_PESQUISA"].nunique()


    def get_concordancia(self) -> float:
        """Retorna a porcentagem de respostas com valor 1 (concordância).

        Retorna 0 se não houver registros.
        """
        df = self.df
        total = len(df)
        if total == 0:
            return 0

        concordancia = df["VALOR_RESPOSTA"].eq(1).sum()
        return (concordancia / total) * 100


    def get_discordancia(self) -> float:
        """Retorna a porcentagem de respostas com valor -1 (discordância).

        Retorna 0 se não houver registros.
        """
        df = self.df
        total = len(df)
        if total == 0:
            return 0

        discordancia = df["VALOR_RESPOSTA"].eq(-1).sum()
        return (discordancia / total) * 100


    def get_desconhecimento(self) -> float:
        """Retorna a porcentagem de respostas com valor 0 (desconhecimento).

        Retorna 0 se não houver registros.
        """
        df = self.df
        total = len(df)
        if total == 0:
            return 0

        desconhecimento = df["VALOR_RESPOSTA"].eq(0).sum()
        return (desconhecimento / total) * 100

    
    def total_respondentes_ano_passado(self): 
        """Compara o total de respondentes com um valor fixo do ano anterior.

        Retorna (percentual_de_comparacao, qtd_respondentes_ano_passado).
        """
        qtd_respondentes_ano_atual = self.get_total_respondentes()
        qtd_respondentes_ano_passado = 1000
        pct_comparacao_ano_atual = (qtd_respondentes_ano_atual / qtd_respondentes_ano_passado - 1) * 100
        return pct_comparacao_ano_atual, qtd_respondentes_ano_passado
    
    def satisfacao_ano_passado(self):
        """Retorna valor fixo de satisfação do ano passado (placeholder)."""
        pct_satisfacao_ano_passado = 40
        return pct_satisfacao_ano_passado
    
    def insatisfacao_ano_passado(self):
        """Retorna valor fixo de insatisfação do ano passado (placeholder)."""
        pct_insatisfacao_ano_passado = 40
        return pct_insatisfacao_ano_passado
    
    def desconhecimento_ano_passado(self):
        """Retorna valor fixo de desconhecimento do ano passado (placeholder)."""
        pct_desconhecimento_ano_passado = 20
        return pct_desconhecimento_ano_passado
    
    def formatacao_curso_setor(self) -> list:
        """Retorna lista formatada de cursos e seus setores.

        O primeiro elemento é 'Todos os cursos'.
        """
        df = self.df[['CURSO', 'SETOR_CURSO']].drop_duplicates()

        opcoes = [
            f"Curso: {row.CURSO} - Setor: {row.SETOR_CURSO}"
            for row in df.itertuples()
        ]
        return ["Todos os cursos"] + sorted(opcoes)

    def df_curso_filtrado_selecionado(self) -> pd.DataFrame:
        """Retorna o DataFrame filtrado pelo curso selecionado.

        Se `self.curso_value` for 'Todos', retorna o DataFrame completo.
        """
        df = self.df
        curso_value = self.curso_value
        if curso_value == 'Todos':
            df_curso = df
        else:
            df_curso = df[df["CURSO"] == curso_value]

        return df_curso
    
    def grafico_distribuicao_total_donut(self):
        """Gera gráfico donut com a distribuição de respostas por curso.

        Retorna (total_respostas, figura) ou None se não houver respostas.
        """
        curso_value = self.curso_value

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.df_curso_filtrado_selecionado()
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

        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        if curso_value == 'Todas':
            fig_donut.update_layout(
                title=f"Distribuição Geral de Respostas: {curso_value}",
                showlegend=False,
                margin=dict(t=40, b=0, l=0, r=0),
                height=400
            )
        else:
            fig_donut.update_layout(
                title={'text': f"Distribuição Geral de Respostas"},
                showlegend=False,
                margin=dict(t=100, b=0, l=0, r=0),
                height=400
            )

        return total_resp, fig_donut
    
    def grafico_resumo_por_eixo(self):
        """Gera um gráfico de barras empilhadas com a distribuição por eixo.

        Retorna uma figura Plotly com porcentagens por resposta em cada eixo.
        """
        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }
        df_filtered = self.df_curso_filtrado_selecionado()

        if df_filtered.empty:
            return None

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
    
    def get_total_respondentes_filtrado(self) -> int:
        """Retorna número de respondentes únicos no DataFrame filtrado."""
        df = self.df_curso_filtrado_selecionado()
        if df.empty:
            return 0
        return df["ID_PESQUISA"].nunique()
    
    def get_total_respostas_filtrado(self) -> int:
        """Retorna o total de linhas/respostas no DataFrame filtrado."""
        df = self.df_curso_filtrado_selecionado()
        return len(df)

    def get_concordancia_filtrado(self):
        """Calcula porcentagem e total de concordância no conjunto filtrado.

        Retorna (percentual, total_concordo). Se vazio, retorna (0, 0).
        """
        df = self.df_curso_filtrado_selecionado()
        total = len(df)

        if total == 0:
            return 0, 0

        total_concordo = df["VALOR_RESPOSTA"].eq(1).sum()
        pct = (total_concordo / total) * 100

        return pct, total_concordo

    def get_discordancia_filtrado(self):
        """Calcula porcentagem e total de discordância no conjunto filtrado.

        Retorna (percentual, total_discordo). Se vazio, retorna (0, 0).
        """
        df = self.df_curso_filtrado_selecionado()
        total = len(df)

        if total == 0:
            return 0, 0

        total_discordo = df["VALOR_RESPOSTA"].eq(-1).sum()
        pct = (total_discordo / total) * 100

        return pct, total_discordo

    def get_desconhecimento_filtrado(self):
        """Calcula porcentagem e total de desconhecimento no conjunto filtrado.

        Retorna (percentual, total_desconheco). Se vazio, retorna (0, 0).
        """
        df = self.df_curso_filtrado_selecionado()
        total = len(df)

        if total == 0:
            return 0, 0

        total_desconheco = df["VALOR_RESPOSTA"].eq(0).sum()
        pct = (total_desconheco / total) * 100

        return pct, total_desconheco

    def grafico_radar_dimensao_curso(self):
        """Gera gráfico radar comparando médias do Curso vs Setor por ID_PERGUNTA.

        Retorna tupla (fig, df_legenda) onde `df_legenda` mapeia ID -> PERGUNTA.
        Se não houver dados ou a dimensão faltar, retorna (None, None).
        """
        dimensao_selecionada = self.dimensao_value

        df_curso = self.df_curso_filtrado_selecionado()
        if df_curso.empty or 'DIMENSAO_NOME' not in df_curso.columns:
            return None, None

        df_curso_dim = df_curso[df_curso['DIMENSAO_NOME'] == dimensao_selecionada]
        if df_curso_dim.empty:
            return None, None

        nome_setor = df_curso['SETOR_CURSO'].iloc[0]
        df_setor_dim = self.df[
            (self.df['SETOR_CURSO'] == nome_setor) &
            (self.df['DIMENSAO_NOME'] == dimensao_selecionada)
        ]

        df_legenda = (
            df_curso_dim[['ID_PERGUNTA', 'PERGUNTA']]
            .drop_duplicates()
            .sort_values('ID_PERGUNTA')
        )

        media_curso = df_curso_dim.groupby('ID_PERGUNTA')['VALOR_RESPOSTA'].mean()
        media_setor = df_setor_dim.groupby('ID_PERGUNTA')['VALOR_RESPOSTA'].mean()

        df_radar = pd.DataFrame({'Curso': media_curso, 'Setor': media_setor}).fillna(0)

        categorias = df_radar.index.astype(str).tolist()
        if len(categorias) == 0:
            return None, None

        categorias = [*categorias, categorias[0]]
        valores_curso = [*df_radar['Curso'].tolist(), df_radar['Curso'].iloc[0]]
        valores_setor = [*df_radar['Setor'].tolist(), df_radar['Setor'].iloc[0]]

        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=valores_setor,
                theta=categorias,
                fill='toself',
                name=f'Média Setor',
                line=dict(color='gray', dash='dot'),
                opacity=0.5,
            )
        )

        fig.add_trace(
            go.Scatterpolar(
                r=valores_curso,
                theta=categorias,
                fill='toself',
                name='Curso',
                line=dict(color='#e74c3c', width=3),
            )
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[-0.5, 1], tickfont=dict(size=9))),
            title=f"Detalhe: {dimensao_selecionada}",
            margin=dict(l=40, r=40, t=50, b=40),
            height=400,
        )

        return fig, df_legenda

    

    
    