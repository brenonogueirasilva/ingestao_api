import os
import json 
import requests

class DirectoryHandler:
    def __init__(self, destination_path: str):
        self.destination_path = destination_path
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)

    def request_to_json_file(self, object_request: requests.Response, name_file: str):
        path_save = f'{self.destination_path}/{name_file}.json' 
        with open(path_save, 'w') as json_file:
            json.dump(object_request.json(), json_file, indent=4)

    def list_dir(self) -> list:
        return os.listdir(self.destination_path)