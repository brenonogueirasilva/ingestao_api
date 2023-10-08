from brasil_api import BrasilApi
from directory_handler import DirectoryHandler

class ApiOrquestrator:
    """
    An API orchestrator class for handling requests, processing responses, and saving data for multiples requests, passing lists on paremeters 

    Args:
        endpoint (str): The API endpoint URL.
        query_parameters (dict): Dictionary of query parameters for API requests.
        path_parameters (list): List of path parameters for API requests (default is [None]).
        token (str): Authentication token for API requests (default is None).
        download_folder (str): The folder where downloaded files will be saved (default is '.').
    """
    def __init__(self, endpoint: str, query_parameters: dict, path_parameters: list = [None] , token: str = None, download_folder: str = '.'):
        self.endpoint = endpoint
        self.query_parameters = query_parameters
        self.path_parameters = path_parameters
        self.token = token
        self.download_folder = download_folder

    def generate_list_query__path_parameters(self) -> list:
        """
        Generate a list of dictionaries with combined query and path parameters.

        Returns:
            list: A list of dictionaries, each containing 'path' and 'query_parameter' keys.
        """
        query_parameter = self.query_parameters.copy()
        for key, value in query_parameter.items():
            query_parameter[key] = [value] 
        df_parameters = pd.DataFrame(query_parameter)
        for column in df_parameters.columns:
            df_parameters = df_parameters.explode(column)
        ls_query_parameters = df_parameters.to_dict(orient='records')
        ls_parameters = []            
        for path in self.path_parameters:
            for query in ls_query_parameters:
                ls_parameters.append( {'path' : path, 'query_parameter' : query} )
        return ls_parameters
    
    def execute_requests_save_file(self):
        """
        Execute API requests, save responses to JSON files.
        """
        directory = DirectoryHandler(self.download_folder)
        ls_query_path_parameters = self.generate_list_query__path_parameters()
        for dict_query_parameters in ls_query_path_parameters:
            obj_brasil_api = BrasilApi(
                endpoint= self.endpoint,
                query_parameter= dict_query_parameters['query_parameter'],
                path_parameter= dict_query_parameters['path'] 
            )
            response = obj_brasil_api.request_get()
            name_file = obj_brasil_api.generate_name_file()
            directory.request_to_json_file(response, name_file)