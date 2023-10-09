import sys
sys.path.append('../src')
from classes.api_orquestrator import ApiOrquestrator


def test_generate_list_query__path_parameters():
    '''
    Test if the list of query or path parameters is correct to be used in Brasil Api Class
    '''
    correct_response = [{'path': 'BA',
  'query_parameter': {'providers': 'dados-abertos-br,gov,wikipedia'}},
 {'path': 'CE',
  'query_parameter': {'providers': 'dados-abertos-br,gov,wikipedia'}}]
    
    orquestrador = ApiOrquestrator(
    endpoint= "ibge/municipios/v1/",
    query_parameters =  { "providers" : "dados-abertos-br,gov,wikipedia"},
    path_parameters = ['BA', 'CE'],
    download_folder= './download/'
)
    response  = orquestrador.generate_list_query__path_parameters()

    assert correct_response == response