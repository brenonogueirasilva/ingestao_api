import shutil
import os 
from unittest.mock import Mock , patch
import pandas as pd

from Class import BrasilApi
from Class import DirectoryHandler
from Class import Postgres


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
        query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameters= ['SP', 'MG' ],
        download_folder= './test_download'  
    )
    query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"}
    path_parameter = 'SP'
    resposta = brasil_api.request(query_parameters, path_parameter)
    assert resposta == None 

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
        query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameters= ['SP', 'MG' ],
        download_folder= './test_download'  
    )
    query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"}
    path_parameter = 'SP'
    resposta = brasil_api.request(query_parameters, path_parameter)
    assert resposta != None 


def test_generate_list_query_parameters():
    '''
    Test if the method can generate a list of dictiaries that not contain a lista, because api request do not accept lists
    '''
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameters = { "par1" : [1,2,3] , "par2" : 2, "par3" : [1,2,3,4,5]},
        path_parameters= ['SP', 'MG' ],
        download_folder= './test_download'  
    )
    dict = brasil_api.generate_list_query_parameters()
    cont_dict =0 
    for item in dict:
        if isinstance(item, list):
            cont_dict += 1
    assert cont_dict == 0
    
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

@patch('requests.get')
def test_execute_requests_save_file(mock_get):
    '''
    Test if the method can execute api and save json using another class
    '''
    requisicao = Mock()
    requisicao.status_code = 200
    requisicao.json = Mock(return_value= [{'chave' : 'valor'}, {'chave2' : 'valor2'}] )
    mock_get.return_value = requisicao

    download_folder = './test_download' 
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameters = { "par1" : 1 , "par2" : 2, "par3" : 5},
        path_parameters= 'MG',
        download_folder= download_folder  
    )
    brasil_api.execute_requests_save_file()
    number_files = os.listdir(download_folder)
    assert len(number_files) > 0
    files = os.listdir(download_folder)
    assert 'json' in files[0]
    shutil.rmtree(download_folder)

    