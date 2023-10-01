import os
import json 
import requests

class DirectoryHandler:
    ''' 
    A class for handling directories and JSON file operations.

    Parameters:
        - destination_path (str): The path to the destination directory.

    Methods:
        - request_to_json_file(object_request: requests.Response, name_file: str):
            Saves the JSON content of a requests.Response object to a file with the specified name.

        - list_dir() -> list:
            Returns a list of files and directories in the destination directory.
    ''' 
    def __init__(self, destination_path: str):
        self.destination_path = destination_path
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)

    def request_to_json_file(self, object_request: requests.Response, name_file: str):
        '''
        Saves the JSON content of a requests.Response object to a JSON file.

        Args:
            object_request (requests.Response): The requests.Response object containing JSON data.
            name_file (str): The name of the JSON file to be saved.
        '''
        path_save = f'{self.destination_path}/{name_file}.json' 
        with open(path_save, 'w') as json_file:
            json.dump(object_request.json(), json_file, indent=4)

    def list_dir(self) -> list:
        '''
        Returns a list of files and directories in the destination directory.

        Returns:
            list: A list of file and directory names.
        '''
        return os.listdir(self.destination_path)