from Class import BrasilApi
from Class import DirectoryHandler
from Class import Postgres

import json 
import pandas as pd

if __name__ == "__main__":
    directory_handler = DirectoryHandler('./download')
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameters= ['SP', 'MG' ],
        download_folder= directory_handler.destination_path  
    )
    brasil_api.execute_requests_save_file()

    with open('./creds.json', 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)

    connector_postgres = Postgres(
        host='localhost', 
        port=5432, 
        database='postgres', 
        user = dados_json['postgres_user'], 
        password = dados_json['postgres_password']
    ) 
    sql_insert = '''
    CREATE TABLE IF NOT EXISTS public.ibge_municipios (
        nome VARCHAR(255),
        codigo_ibge INT,
        path VARCHAR(255)
    );
    '''
    connector_postgres.create_or_delete_table(sql_insert)

    for item in directory_handler.list_dir_complete_path():
        df = directory_handler.json_to_dataframe(path=item)
        connector_postgres.insert_df(df, 'ibge_municipios')

    sql_select = "select * from public.ibge_municipios"
    print(connector_postgres.select(sql_select)) 

    sql_delete = "delete from public.ibge_municipios"
    connector_postgres.create_or_delete_table(sql_select)
