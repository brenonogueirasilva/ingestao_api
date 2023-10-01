import json
import os 
from unittest.mock import Mock , patch
import pandas as pd

import api_poo as api 

#Testar metodo request, status code == 200
@patch('requests.get')
def test_request_status_code(mock_get):

    requisicao = Mock()
    requisicao.status_code = 200
    mock_get.return_value = requisicao

    api_teste = api.Api(
    url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
    download_folder='./downloads/',
    token= 'token',
    par_mes_ano_inicio="01/2023",
    par_mes_ano_fim="01/2023",
    par_orgao_superior= [ 41000,  42000 ] ,
    par_uf= "SP"
    )
    resposta = api_teste.request(1, 4100)
    assert resposta.status_code == 200 

#Testar metodo request, json diferente de vazio
@patch('requests.get')
def test_request_json(mock_get):

    with open('./downloads/recursos_pag(1)_orgao(41000).json', 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)
    requisicao = Mock()
    requisicao.status_code = 200
    requisicao.json = Mock(return_value=dados_json)
    mock_get.return_value = requisicao

    api_teste = api.Api(
    url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
    download_folder='./downloads_2/',
    token= 'token',
    par_mes_ano_inicio="01/2023",
    par_mes_ano_fim="01/2023",
    par_orgao_superior= [ 41000,  42000 ] ,
    par_uf= "SP"
    )
    resposta = api_teste.request(1, 4100)
    assert len(resposta.json()) >= 1 

#Testar metodo save_json, algum arquivo esta sendo criado na pasta de downloads ?
def test_save_json():

    with open('./downloads/recursos_pag(1)_orgao(41000).json', 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)
    class Dados:
        def __init__(self):
            pass 
        def json(self):
            return dados_json 
    
    dados = Dados()
    nome_arquivo = 'teste'

    api_teste = api.Api(
    url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
    download_folder='./downloads_2/',
    token= 'token',
    par_mes_ano_inicio="01/2023",
    par_mes_ano_fim="01/2023",
    par_orgao_superior= [ 41000,  42000 ] ,
    par_uf= "SP"
    )
    api_teste.save_json(nome_arquivo, dados)
    assert  nome_arquivo+'.json' in os.listdir('./downloads_2')


def custom_side_effect(*args, **kwargs):
    with open('./downloads/recursos_pag(1)_orgao(41000).json', 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)
    
    pagina = (kwargs['params']['pagina'])
    if pagina < 5 :
        mock_requisicao =Mock()
        mock_requisicao.status_code = 200
        mock_requisicao.content = [1,2,3,4,5]
        mock_requisicao.json = Mock(return_value=dados_json)
        return mock_requisicao
    else:
        mock_requisicao =Mock()
        mock_requisicao.status_code = 200
        mock_requisicao.content = []
        mock_requisicao.json = Mock(return_value=None)
        return mock_requisicao

#Testando o metodo execute_requests_save_json, ele e capaz de fazer a paginacao e rodar pra mais de uma pagina?
@patch('requests.get')
def test_execute_requests_save_json(mock_get):

    mock_get.side_effect = custom_side_effect

    api_teste = api.Api(
    url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
    download_folder='./downloads_2/',
    token= 'token',
    par_mes_ano_inicio="01/2023",
    par_mes_ano_fim="01/2023",
    par_orgao_superior= [ 41000,  42000 ] ,
    par_uf= "SP"
    )
    api_teste.execute_requests_save_json()
    assert len(os.listdir('./downloads_2/')) > 2
    assert api_teste.requisicoes <= api_teste.limite_requisicoes

#Testando o metodo json_to_df
def test_json_to_df():

    api_teste = api.Api(
    url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
    download_folder='./downloads_2/',
    token= 'token',
    par_mes_ano_inicio="01/2023",
    par_mes_ano_fim="01/2023",
    par_orgao_superior= [ 41000,  42000 ] ,
    par_uf= "SP"
    )
    df = api_teste.json_to_df()
    assert isinstance(df, pd.DataFrame)


