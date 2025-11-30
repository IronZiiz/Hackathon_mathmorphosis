from services.DataLoader  import DataLoader
import pandas as pd
 
class AvaliacaoDosCursosService(DataLoader): 
    def __init__(self):
        super().__init__()
    def get_total_respondentes(self, path: str) -> int:
        df = pd.read_csv(path)
        return df["ID_PESQUISA"].nunique()
    def get_concordancia(self, path: str) -> float:
        df = pd.read_csv(path)
        total = len(df)
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return (concordancia / total) * 100
    def get_discordancia(self, path: str) -> float:
        df = pd.read_csv(path)
        total = len(df)
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])
        return (discordancia / total) * 100
    def get_desconhecimento(self, path: str) -> float:
        df = pd.read_csv(path)
        total = len(df)
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return (desconhecimento / total) * 100
    def get_concordancia_total(self, path: str) -> int:
        df = pd.read_csv(path)
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return concordancia
    def get_discordancia_total(self, path: str) -> int:
        df = pd.read_csv(path)
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])
        return discordancia
    def get_desconhecimento_total(self, path: str) -> int:
        df = pd.read_csv(path)
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return desconhecimento
    def curso_selecionado(self, path: str, curso_value: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df_curso = df[df["CURSO"] == curso_value]
        return df_curso