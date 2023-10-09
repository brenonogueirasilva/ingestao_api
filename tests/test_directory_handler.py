from unittest.mock import Mock , patch
import pandas as pd
import shutil
import os
import json
import pandas as pd
import tempfile
import sys
sys.path.append('../src')
from classes.directory_handler import DirectoryHandler

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
        
    with tempfile.TemporaryDirectory() as tmpdirname:
        folder = "download_folder"
        temp_folder = rf"{tmpdirname}\{folder}"

        object_request = MockRequest()
        download_folder = temp_folder
        directory_handler =DirectoryHandler(download_folder)
        directory_handler.request_to_json_file(object_request, 'teste.json')
        files = os.listdir(download_folder)
        assert 'json' in files[0]

def test_request_to_json_envelope_file():
    '''
    Test if can write a json file with an request object
    '''
    class MockRequest:
        def __init__(self) -> None:
            pass
        def json(self):
            dict = {'chave' : 'valor', 'chave2' : 'valor2'}
            return dict
        
    envelope = {
    "envelope": {
        "endpoint": "ibge/municipios/v1/",
        "path": "BA",
        "providers": "dados-abertos-br,gov,wikipedia"
    }}
        
    with tempfile.TemporaryDirectory() as tmpdirname:
        folder = "download_folder"
        temp_folder = rf"{tmpdirname}\{folder}"

        object_request = MockRequest()
        download_folder = temp_folder
        directory_handler =DirectoryHandler(download_folder)
        directory_handler.request_to_json_envelope_file(object_request, envelope, 'teste.json')
        files = os.listdir(download_folder)
        assert 'json' in files[0]

def test_list_dir():
    '''
    Test if the method can list all list paths on the dir
    '''
    download_folder = '.'
    directory_handler =DirectoryHandler(download_folder)
    list_files = directory_handler.list_dir()
    assert list_files ==  os.listdir(download_folder)


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
    with tempfile.TemporaryDirectory() as tmpdirname:
        folder = "download_folder"
        temp_folder = rf"{tmpdirname}\{folder}"

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

        with tempfile.TemporaryDirectory() as tmpdirname:
            folder = "download_folder"
            temp_dir = str(tmpdirname).replace('\\' , '/')
            temp_dir = f"{temp_dir}/{folder}/"

            directory_handler =DirectoryHandler(temp_dir)
            with open(temp_dir + 'ibge_municipios_path(MG).json' , 'w') as json_file:
                    json.dump( dict_json, json_file, indent=4)

            path = f"{temp_dir}ibge_municipios_path(MG).json"
            df = directory_handler.json_to_dataframe(path)
            assert isinstance(df, pd.DataFrame) 

def test_json_envelope_to_dataframe():
    '''
    Test if json turns into dataframe
    '''
    with tempfile.TemporaryDirectory() as tmpdirname:
        folder = "download_folder"
        temp_folder = rf"{tmpdirname}\{folder}"

        dict_json = {
    "envelope": {
        "endpoint": "ibge/municipios/v1/",
        "path": "BA",
        "providers": "dados-abertos-br,gov,wikipedia"
    },
    "content": [
        {
            "nome": "ABAIRA",
            "codigo_ibge": "2900108"
        }] }

        with tempfile.TemporaryDirectory() as tmpdirname:
            folder = "download_folder"
            temp_dir = str(tmpdirname).replace('\\' , '/')
            temp_dir = f"{temp_dir}/{folder}/"

            directory_handler =DirectoryHandler(temp_dir)
            with open(temp_dir + 'ibge_municipios_path(MG).json' , 'w') as json_file:
                    json.dump( dict_json, json_file, indent=4)

            path = f"{temp_dir}ibge_municipios_path(MG).json"
            df = directory_handler.json_envelope_to_dataframe(path)
            assert isinstance(df, pd.DataFrame)    


