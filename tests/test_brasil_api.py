import shutil
import os 
from unittest.mock import Mock , patch
import pandas as pd
import sys 
sys.path.append('../src')
from classes.brasil_api import BrasilApi


@patch('requests.get')
def test_method_request_1(mock_get):
    '''
    Test if method request return None when status_code is not 200
    '''
    requisicao = Mock()
    requisicao.status_code = 400
    mock_get.return_value = requisicao 

    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameter = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameter= 'MG'  
    )
    response = brasil_api.request_get()
    assert response == None 


@patch('requests.get')
def test_method_request_2(mock_get):
    '''
    Test if method return not None when status_code is 200
    '''
    requisicao = Mock()
    requisicao.status_code = 200
    mock_get.return_value = requisicao 

    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameter = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameter= 'MG'  
    )
    response = brasil_api.request_get()
    assert response != None 

    
def test_generate_name_file():
    '''
    Test if method can generate a name with list parameters
    '''
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameters = { "par1" : [1,2,3] , "par2" : 2, "par3" : [1,2,3,4,5]},
        path_parameters= ['SP', 'MG' ],
        download_folder= './test_download'  
    )
    query = { "par1" : 2 , "par2" : 2, "par3" : 4}
    path_parameters= 'MG'
    name = brasil_api.generate_name_file(query, path_parameters) 
    assert 'path' in name and 'MG' in name and 'par1' in name and '2' in name and 'par3' in name and '4' in name

def test_generate_envelope():
    '''
    Test if method return not None when status_code is 200
    '''
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameter = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameter= 'MG'  
    )
    envelope = brasil_api.generate_envelope()
    assert envelope == {'envelope': {'endpoint': 'ibge/municipios/v1/', 'path': 'MG', 'providers': 'dados-abertos-br,gov,wikipedia'}}

    