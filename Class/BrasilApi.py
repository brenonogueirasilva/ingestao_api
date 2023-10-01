import requests
import pandas as pd
from .DirectoryHandler import DirectoryHandler

class BrasilApi:
    '''
    Class for interacting with the BrasilAPI (https://brasilapi.com.br/).

    Parameters:
        - endpoint (str): The specific API endpoint you want to access.
        - query_parameters (str): Query parameters for the request in string format.
        - path_parameters (dict, optional): Path parameters for the request in a dictionary.
        - token (str, optional): An authentication token (if applicable) to access restricted resources.
        - download_folder (str, optional): The destination directory to save downloaded files (default is the current directory).

    Methods:
        - request(query_parameter: dict, path_parameter: str) -> requests.Response:
            Makes a request to the BrasilAPI with the specified parameters.
        
        - generate_list_query_parameters() -> list:
            Generates a list of query parameters from parameters that are list
        
        - generate_name_file(query: dict, path: str = None) -> str:
            Generates a file name based on the query and path parameters specified.

        - execute_requests_save_file():
            Executes requests to the API and saves the results to JSON files using the specified query and path parameters.
    '''
    def __init__(self, endpoint: str, query_parameters: str, path_parameters: dict = None, token: str = None, download_folder: str = '.'):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.query_parameters = query_parameters
        self.path_parameters = path_parameters
        self.token  = token
        self.download_folder = download_folder

    def request(self, query_parameter : dict, path_parameter: str) -> requests.Response:
        '''
        Makes a request to the BrasilAPI with the specified parameters.

        Args:
            query_parameter (dict): Query parameters for the request.
            path_parameter (str): Path parameters for the request.

        Returns:
            requests.Response: The response object of the request.
        '''
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
        '''
        Generates a list of query parameters from the provided string parameter.

        Returns:
            list: A list of dictionaries representing the query parameters.
        '''
        query_parameter = self.query_parameters.copy()
        for key, value in query_parameter.items():
            query_parameter[key] = [value] 
        df_parameters = pd.DataFrame(query_parameter)
        for column in df_parameters.columns:
            df_parameters = df_parameters.explode(column)
        ls_parameters = df_parameters.to_dict(orient='records')
        return ls_parameters
    
    def generate_name_file(self, query: dict, path: str= None) -> str:
        '''
        Generates a file name based on the query and path parameters specified.

        Args:
            query (dict): Query parameters for the request.
            path (str, optional): Path parameters for the request.

        Returns:
            str: The generated file name.
        '''
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
        ''' 
        Executes requests to the API and saves the results to JSON files,
        using the specified query and path parameters.
        '''
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
    
    