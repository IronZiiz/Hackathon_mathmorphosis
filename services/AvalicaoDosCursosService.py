from services.DataLoader  import DataLoader
import pandas as pd
 
class AvaliacaoDosCursosService(DataLoader): 
    def __init__(self,
                df_load_dados_curso = None):
        
        if df_load_dados_curso is None:
            df_load_dados_curso = DataLoader.load_dados_curso()

        self.df = df_load_dados_curso

    def get_total_respondentes(self) -> int:
        return self.df["ID_PESQUISA"].nunique() # Será que essa quantidade é de fato os respondentes?
    
    def get_concordancia(self) -> float:
        df = self.df
        total = len(df)
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return (concordancia / total) * 100
    
    def get_discordancia(self) -> float:
        df = self.df
        total = len(df)
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])

        return (discordancia / total) * 100
    
    def get_desconhecimento(self) -> float:
        df = self.df
        total = len(df)
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return (desconhecimento / total) * 100
    
    def get_concordancia_total(self) -> int:
        df = self.df
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return concordancia
    
    def get_discordancia_total(self) -> int:
        df = self.df
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])
        return discordancia
    
    def get_desconhecimento_total(self) -> int:
        df = self.df
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return desconhecimento
    
    def curso_selecionado(self, curso_value: str) -> pd.DataFrame:
        df = self.df
        df_curso = df[df["CURSO"] == curso_value]
        return df_curso