
class LoginService:
    """
    Serviço responsável pela lógica de autenticação.
    """

    def __init__(
        self,
        username=None,
        password=None,
        valid_username="admin",
        valid_password="123",
        submitted_value = None
    ):
        self.username = username
        self.password = password

        self.valid_username = valid_username
        self.valid_password = valid_password

        self.submitted_value = submitted_value

    def authenticate(self) -> dict:
        """
        Valida as credenciais e retorna um objeto contendo:
        - success: True/False
        - message: mensagem amigável
        """
        if self.username == self.valid_username and self.password == self.valid_password:
            return {
                "success": True,
                "message": "Login realizado com sucesso!"
            }
        else:
            return {
                "success": False,
                "message": "Usuário ou senha incorretos."
            }
        
  

