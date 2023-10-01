import requests
import pandas as pd
import DirectoryHandler

class BrasilApi:
    def __init__(self, endpoint: str, query_parameters: str, path_parameters: dict = None, token: str = None, download_folder: str = '.'):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.query_parameters = query_parameters
        self.path_parameters = path_parameters
        self.token  = token
        self.download_folder = download_folder

    def request(self, query_parameter : dict, path_parameter: str) -> requests.Response:
        if self.token is not None:
            header = {
                "chave-api-dados" : self.token
            }
        else:
            header = None

        if path_parameter is None:
            complete_url = self.url + self.endpoint
        else:
            complete_url = self.url + self.endpoint + path_parameter

        try:
            response = requests.get(url= complete_url, headers= header, params= query_parameter)
            if response.status_code == 200:
                return response
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print("Ocorreu um erro ao fazer a solicitação:")
            print(error)

    def generate_list_query_parameters(self) -> list:
        query_parameter = self.query_parameters.copy()
        for key, value in query_parameter.items():
            query_parameter[key] = [value] 
        df_parameters = pd.DataFrame(query_parameter)
        for column in df_parameters.columns:
            df_parameters = df_parameters.explode(column)
        ls_parameters = df_parameters.to_dict(orient='records')
        return ls_parameters
    
    def generate_name_file(self, query: dict, path: str= None) -> str:
        name_file = self.endpoint.split('/')
        name_file = list(filter(lambda item : 'v' not in item and len(item) > 1, name_file))
        name_file = "_".join(name_file)
        if path is not None:
            name_file = f"{name_file}_path({path})" 

        list_queries = []
        for key, value in self.query_parameters.items():
            if isinstance(value, list):
                list_queries.append(key)
        if len(list_queries) > 0:
            for item in list_queries:
                query_value = query[item]
                name_file = f"{name_file}_query({query_value})" 
        return name_file
    
    def execute_requests_save_file(self):
        directory = DirectoryHandler(self.download_folder)
        ls_query_parameters = self.generate_list_query_parameters()
        path_parameters = self.path_parameters
        if path_parameters is None:
            for query in ls_query_parameters:
                response = self.request(query_parameter= query)
                name = self.generate_name_file(query)
                directory.request_to_json_file(response, name)
        else:
            if not isinstance(path_parameters, list):
                path_parameters = [path_parameters]
            for path in path_parameters:
                for query in ls_query_parameters:
                    response = self.request(query_parameter= query , path_parameter= path)
                    name = self.generate_name_file(query, path)
                    directory.request_to_json_file(response, name)
    
    