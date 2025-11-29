from services.DataLoader  import DataLoader


class AvaliacaoInstitucionalService(DataLoader): 
    def __init__(self,
                 eixos_value = None,
                 perguntas_value = None,
                 ):

        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value


    def total_respondentes_ano_atual(self): 
        
        return 
    
    def total_respondentes_ano_passado(self): 
        return 

