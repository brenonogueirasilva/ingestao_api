from unittest.mock import Mock , patch
import pandas as pd
import shutil
import os

from Class import DirectoryHandler


#Testa se metodo request so retorna objeto com metodo 200
def test_request_to_json_file():

    class MockRequest:
        def __init__(self) -> None:
            pass
        def json(self):
            dict = {'chave' : 'valor', 'chave2' : 'valor2'}
            return dict
        
    object_request = MockRequest()
    download_folder = './test_download'
    directory_handler =DirectoryHandler(download_folder)
    directory_handler.request_to_json_file(object_request, 'teste.json')
    files = os.listdir(download_folder)
    assert 'json' in files[0]
    shutil.rmtree(download_folder)