from unittest.mock import Mock , patch
import pandas as pd
import shutil
import os

from Class import DirectoryHandler

def test_request_to_json_file():
    '''
    Test if can write a json file with an request object
    '''
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

def test_list_dir():
    '''
    Test if the method can list all list paths on the dir
    '''
    download_folder = './download'
    directory_handler =DirectoryHandler(download_folder)
    list_files = directory_handler.list_dir()
    assert list_files ==  os.listdir(download_folder)

def test_dir_complete_path():
    '''
    Test if the method can list a complete path on the dir
    '''
    download_folder = './Class'
    directory_handler =DirectoryHandler(download_folder)
    list_files = directory_handler.list_dir_complete_path()
    example_path = './Class/Postgres.py'
    assert example_path in list_files


