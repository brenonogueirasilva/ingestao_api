class BrasilApi:
    def __init__(self, endpoint, query_parameters, path_parameters = None, token = None, download_folder = '.'):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.query_parameters = query_parameters
        self.path_parameters = path_parameters
        self.token  = token
        self.download_folder = download_folder
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