import os
import json 

class DirectoryHandler:
    def __init__(self, destination_path):
        self.destination_path = destination_path

    def request_to_json_file(self, object_request, name_file):
        path_save = f'{self.destination_path}/{name_file}.json' 
        with open(path_save, 'w') as json_file:
            json.dump(object_request.json(), json_file, indent=4)