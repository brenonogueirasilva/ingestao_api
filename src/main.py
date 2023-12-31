import json 
import logging

from classes.api_orquestrator import ApiOrquestrator
from classes.postgres import Postgres
from classes.directory_handler import DirectoryHandler

if __name__ == "__main__":
    logging.basicConfig(filename='/code/logs.log', level=logging.DEBUG, format= "%(asctime)s :: %(levelname)s :: %(message)s :: %(filename)s :: %(lineno)d ", )
    orquestrador = ApiOrquestrator(
    endpoint= "ibge/municipios/v1/",
    query_parameters =  { "providers" : "dados-abertos-br,gov,wikipedia"},
    path_parameters = ['MG' , 'SP', 'SE'],
    download_folder= '/code/download/'
)
    logging.info('Beggining Request to API')
    list_requests = orquestrador.generate_list_query__path_parameters()
    orquestrador.execute_requests_envelope_save_file()
    logging.info('Request to API done with sucess')

    connector_postgres = Postgres(
        host='postgres_ingestao_por_api', 
        port=5432, 
        database='postgres', 
        user = 'postgres', 
        password = 'postgres'
    ) 

    sql_insert = '''
    CREATE TABLE IF NOT EXISTS public.ibge_municipios (
        nome VARCHAR(255),
        codigo_ibge INT,
        path VARCHAR(255),
        endpoint VARCHAR(255),
        providers VARCHAR(255)
    );
    '''
    connector_postgres.create_or_delete_table(sql_insert)

    directory_handler = DirectoryHandler('../download')
    for item in directory_handler.list_dir_complete_path():
        df = directory_handler.json_envelope_to_dataframe(path=item)
        connector_postgres.insert_df(df, 'ibge_municipios')
    logging.info('Pipeline done with sucess')

