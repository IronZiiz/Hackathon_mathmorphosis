import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoDasDisciplinasService(DataLoader): 
    def __init__(self,
                df_load_dados_avaliacao_disciplinas_presencial = None,
                df_load_dados_avaliacao_disciplinas_EAD = None, 
                disciplina_value = None,
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
    

        
    
