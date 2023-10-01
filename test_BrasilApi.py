import json
import os 
from unittest.mock import Mock , patch
import pandas as pd

from Class import BrasilApi
from Class import DirectoryHandler
from Class import Postgres


#Testa se metodo request so retorna objeto com metodo 200
@patch('requests.get')
def test_method_request_1(mock_get):

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

#Testa se metodo request so retorna objeto com metodo 200
@patch('requests.get')
def test_method_request_2(mock_get):

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
