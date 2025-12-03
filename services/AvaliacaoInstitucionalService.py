import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoInstitucionalService(DataLoader):
    """Serviço para análise dos dados de avaliação institucional.

    Fornece métodos para filtrar os dados, calcular métricas de
    respondentes/respostas e gerar gráficos de distribuição e resumo.
    """
    def __init__(
        self, 
        eixos_value=None,
        perguntas_value=None,
        dimensao_value = None,
        df_load_dados_institucional=None,
    ):
        """Inicializa o serviço com filtros e DataFrame opcional.

        Parâmetros
        ----------
        eixos_value, perguntas_value, dimensao_value : opcionais
            Valores usados para filtrar os dados nas visualizações.
        df_load_dados_institucional : pd.DataFrame | None
            DataFrame com os dados institucionais. Se None, é carregado via DataLoader.
        """
        if df_load_dados_institucional is None:
            df_load_dados_institucional = DataLoader.load_dados_institucional()

        self.df_load_dados_institucional = df_load_dados_institucional
        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value
        self.dimensao_value = dimensao_value
    
    def formatar_eixos(self) -> list:
        """Retorna lista de eixos disponíveis (iniciando por 'Todos')."""
        df = self.df_load_dados_institucional
        list_eixos = list(df['EIXO_NOME'].unique())

        return ['Todos'] + list_eixos
    
    def filtrar_dados_institucionais(self):
        """Filtra os dados institucionais por eixo e pergunta.

        Retorna um DataFrame filtrado de acordo com `self.eixos_value` e
        `self.perguntas_value`. Se o valor for 'Todos' ou vazio, não aplica
        o respectivo filtro.
        """
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
            df_filtered = df[df["EIXO_NOME"].isin(eixo_value)].sort_values(by="Ordem")

        if pergunta_value and "Todos" not in pergunta_value:
            perguntas_extraidas = [p.split(" - ", 1)[1] for p in pergunta_value]
            df_filtered = df_filtered[df_filtered["PERGUNTA"].isin(perguntas_extraidas)]

        return df_filtered
    
    def total_respondentes_ano_atual(self): 
        """Retorna a quantidade de respondentes únicos no ano atual."""
        df = self.df_load_dados_institucional
        qtd_respondentes_atual = df['ID_PESQUISA'].nunique()
        return qtd_respondentes_atual
    
    def total_respondentes_ano_passado(self): 
        """Compara o número de respondentes com um valor fixo do ano anterior.

        Retorna (percentual_de_comparacao, qtd_respondentes_ano_passado).
        """
        qtd_respondentes_ano_atual = self.total_respondentes_ano_atual()
        qtd_respondentes_ano_passado = 500
        pct_comparacao_ano_atual = (qtd_respondentes_ano_atual / qtd_respondentes_ano_passado - 1) * 100
        return pct_comparacao_ano_atual, qtd_respondentes_ano_passado
    
    def total_respostas_ano_atual(self): 
        """Retorna o total de respostas registradas no ano atual."""
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = len(df)
        return total_respostas

    def satisfacao_ano_atual(self):
        """Retorna a porcentagem de respostas 'Concordo' no ano atual."""
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual()

        pct_satisfacao_ano_atual = (df['RESPOSTA'].eq('Concordo').sum() / total_respostas) * 100

        return pct_satisfacao_ano_atual
    
    def satisfacao_ano_passado(self): 
        """Retorna valor fixo de satisfação para o ano passado (placeholder)."""
        pct_satisfacao_ano_passado = 50
        return pct_satisfacao_ano_passado
    
    def satisfacao_ano_passado(self):
        """(Sobrescrito) Retorna valor fixo de satisfação anterior."""
        pct_satisfacao_ano_passado = 40
        return pct_satisfacao_ano_passado
    
    def insatisfacao_ano_passado(self):
        """Retorna valor fixo de insatisfação no ano passado (placeholder)."""
        pct_insatisfacao_ano_passado = 40
        return pct_insatisfacao_ano_passado
    
    def desconhecimento_ano_passado(self):
        """Retorna valor fixo de desconhecimento no ano passado (placeholder)."""
        pct_desconhecimento_ano_passado = 20
        return pct_desconhecimento_ano_passado
    
    def insatisfacao_ano_atual(self):
        """Retorna a porcentagem de respostas 'Discordo' no ano atual."""
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual()
        pct_insatisfacao_ano_atual = (df['RESPOSTA'].eq('Discordo').sum() / total_respostas) * 100
        return pct_insatisfacao_ano_atual
           
    def desconhecimento_ano_atual(self): 
        """Retorna a porcentagem de respostas 'Desconheço' no ano atual."""
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual()
        pct_desconhecimento_ano_atual = (df['RESPOSTA'].eq('Desconheço').sum() / total_respostas) * 100
        return pct_desconhecimento_ano_atual
    
    def grafico_distribuicao_total_donut(self):
        """Gera um gráfico donut com a distribuição geral de respostas.

        Retorna (total_respostas, figura) ou None se não houver respostas.
        """
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

        fig_donut.update_traces(textposition='inside', textinfo='percent+label')

        fig_donut.update_layout(
            title="Distribuição Geral de Respostas",
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            height=400
        )

        return total_resp, fig_donut
    
    def get_respondentes_filtrados(self):
        """Retorna (respondentes_unicos, total_respostas) após aplicar filtros."""
        df = self.filtrar_dados_institucionais()
        if df.empty or 'ID_PESQUISA' not in df.columns:
            return 0, 0

        total_respondentes = df['ID_PESQUISA'].nunique()
        total_respostas = len(df)

        return total_respondentes, total_respostas

    def get_concordancia_filtrado(self):
        """Retorna (percentual_concordancia, total_concordancia) para os dados filtrados."""
        df = self.filtrar_dados_institucionais()
        _, total_respostas = self.get_respondentes_filtrados()

        if df.empty or 'RESPOSTA' not in df.columns:
            return 0, 0

        total_concordo = df['RESPOSTA'].eq('Concordo').sum()

        if total_respostas == 0:
            return 0, 0

        pct = (total_concordo / total_respostas) * 100
        return pct, total_concordo

    def get_discordancia_filtrado(self):
        """Retorna (percentual_discordancia, total_discordancia) para os dados filtrados."""
        df = self.filtrar_dados_institucionais()
        _, total_respostas = self.get_respondentes_filtrados()

        if df.empty or 'RESPOSTA' not in df.columns:
            return 0, 0

        total_discordo = df['RESPOSTA'].eq('Discordo').sum()

        if total_respostas == 0:
            return 0, 0

        pct = (total_discordo / total_respostas) * 100
        return pct, total_discordo

    def get_desconhecimento_filtrado(self):
        """Retorna (percentual_desconhecimento, total_desconhecimento) para os dados filtrados."""
        df = self.filtrar_dados_institucionais()
        _, total_respostas = self.get_respondentes_filtrados()

        if df.empty or 'RESPOSTA' not in df.columns:
            return 0, 0

        total_desc = df['RESPOSTA'].eq('Desconheço').sum()

        if total_respostas == 0:
            return 0, 0

        pct = (total_desc / total_respostas) * 100
        return pct, total_desc

    def grafico_resumo_por_eixo(self):
        """Gera um gráfico de barras empilhadas com a distribuição por eixo.

        Retorna o objeto de figura Plotly ou None se não houver dados.
        """
        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.filtrar_dados_institucionais()

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

        fig_bar.update_traces(textposition="inside", insidetextanchor="middle")

        fig_bar.update_layout(
            title='Distribuição de respostas por eixos',
            xaxis_title="Eixo",
            yaxis_title="% das Respostas",
            legend_title="",
            margin=dict(l=10, r=10, t=45, b=0),
            yaxis=dict(range=[0, 100]),
            xaxis=dict(tickangle=10)
        )

        return fig_bar

    def preparar_dados_unidade_gestora(self):
        """Prepara DataFrame com contagem de respostas por unidade gestora."""
        df = self.filtrar_dados_institucionais()
        df = df[['ID_PESQUISA', 'UNIDADE GESTORA']]
        df = df.dropna(subset=['UNIDADE GESTORA'])

        dataframe_fig = (
            df.groupby('UNIDADE GESTORA')
            .size()
            .reset_index(name='TOTAL_RESPOSTAS')
            .sort_values('TOTAL_RESPOSTAS', ascending=True)
        )

        return dataframe_fig

    def grafico_barra_unidade_gestora(self):
        """Gera gráfico de barras horizontais com top 10 unidades gestoras."""
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
        """Gera gráfico donut mostrando participação do top 10 unidades gestoras."""
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
                marker=dict(colors=["#3498db", "#95a5a6"]),
                insidetextorientation='horizontal',
                rotation=68
            )
        ])

        fig_donut.update_layout(
            showlegend=False,
            title="Participação do TOP 10 no Total de Respondentes",
            height=500
        )

        return fig_donut

    def grafico_saldo_opiniao_dimensao(self):
        """Gera figura com saldo de opinião por pergunta para a dimensão selecionada.

        Se `self.dimensao_value` não estiver definida ou a coluna necessária
        estiver ausente, retorna None.
        """
        df = self.df_load_dados_institucional.copy()

        dim_sel = self.dimensao_value
        if not dim_sel:
            return None

        if 'DIMENSAO_NOME' not in df.columns:
            return None

        df_filtered = df[df["DIMENSAO_NOME"] == dim_sel]

        if df_filtered.empty:
            return None

        stats_pct = pd.crosstab(
            df_filtered['PERGUNTA'],
            df_filtered['RESPOSTA'],
            normalize='index'
        ) * 100

        for col in ['Concordo', 'Discordo', 'Desconheço']:
            if col not in stats_pct.columns:
                stats_pct[col] = 0.0

        stats_pct = stats_pct.sort_values('Concordo', ascending=True)

        questions = stats_pct.index.tolist()
        concordo_list = stats_pct['Concordo'].tolist()
        discordo_list = stats_pct['Discordo'].tolist()
        desconheco_list = stats_pct['Desconheço'].tolist()

        desconheco_metade = [x / 2 for x in desconheco_list]
        desconheco_metade_neg = [-x for x in desconheco_metade]
        discordo_neg_list = [-x for x in discordo_list]

        hover_desconheco = [f"Desconheço: {x:.1f}%" for x in desconheco_list]
        text_desconheco = [f"{x:.1f}%" if x > 1 else "" for x in desconheco_list]

        def quebrar_texto(texto, max_chars=60):
            if len(texto) <= max_chars:
                return texto
            import textwrap
            return "<br>".join(textwrap.wrap(texto, width=max_chars))

        questions_formatted = [quebrar_texto(q) for q in questions]

        fig_div = go.Figure()

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade_neg,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=True,
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly'
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=False,
            text=text_desconheco, textposition='inside',
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly'
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=discordo_neg_list,
            name='Discordo', orientation='h', marker_color='#e74c3c',
            text=[f"{x:.1f}%" if x > 1 else "" for x in discordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Discordância: {x:.1f}%" for x in discordo_list]
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=concordo_list,
            name='Concordo', orientation='h', marker_color='#2ecc71',
            text=[f"{x:.1f}%" if x > 1 else "" for x in concordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Concordância: {x:.1f}%" for x in concordo_list]
        ))

        fig_div.update_layout(
            barmode='relative',
            title=f"Saldo de Opinião: {dim_sel}",
            xaxis_title="% Rejeição <---> % Aprovação",
            yaxis=dict(title=""),
            bargap=0.3,
            legend_title_text='Sentimento',
            height=max(400, len(questions) * 60 + 150),
            margin=dict(l=10, r=10, t=80, b=20)
        )

        fig_div.add_vline(x=0, line_width=1, line_color="black", opacity=0.3)

        return fig_div
            
            