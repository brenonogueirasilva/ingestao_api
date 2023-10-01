class BrasilApi:
    def __init__(self, endpoint, parameters, token = None):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.parameters = parameters 
        self.token  = token
        self.requisicoes = 0
        self.limite_requisicoes = 3

    def request(self):
        if self.token is not None:
            header = {
                "chave-api-dados" : self.token
            }
        else:
            header = None
        try:
            response = requests.get(self.url, params=self.parameters, headers= header)
            if response.status_code == 200:
                return response
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print("Ocorreu um erro ao fazer a solicitação:")
            print(error)