
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