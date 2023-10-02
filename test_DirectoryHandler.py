from unittest.mock import Mock , patch
import pandas as pd
import shutil
import os
import json
import pandas as pd

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

def test_api_information():
    '''
    Test if return a dict with information about api (path or query)
    '''
    example_folder = './example_folder/'
    if not os.path.exists(example_folder):
        os.mkdir(example_folder)
    with open(example_folder + 'ibge_municipios_path(MG).json' , 'w') as json_file:
            json.dump( {'chave1' : 'valor1', 'chave2' : 'valor2'}, json_file, indent=4)
    path = './example_folder/ibge_municipios_path(MG).json'
    directory_handler =DirectoryHandler(example_folder)
    name = directory_handler.dict_api_information(path)
    assert {'path': 'MG'} == name 
    shutil.rmtree(example_folder)

def test_json_to_dataframe():
    '''
    Test if json turns into dataframe
    '''
    example_folder = './example_folder/'
    if not os.path.exists(example_folder):
        os.mkdir(example_folder)
    dict_json = [
    {
        "nome": "ABADIA DOS DOURADOS",
        "codigo_ibge": "3100104"
    },
    {
        "nome": "ABAETE",
        "codigo_ibge": "3100203"
    },
    {
        "nome": "ABRE CAMPO",
        "codigo_ibge": "3100302"
    }]
    with open(example_folder + 'ibge_municipios_path(MG).json' , 'w') as json_file:
            json.dump( dict_json, json_file, indent=4)

    path= './example_folder/ibge_municipios_path(MG).json'
    directory_handler =DirectoryHandler(example_folder)
    df = directory_handler.json_to_dataframe(path)
    assert isinstance(df, pd.DataFrame) 

    


