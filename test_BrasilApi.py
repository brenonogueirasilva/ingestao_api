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


    


