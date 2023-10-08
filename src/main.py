import json 

from api_orquestrator import ApiOrquestrator
from postgres import Postgres
from directory_handler import DirectoryHandler

if __name__ == "__main__":
    orquestrador = ApiOrquestrator(
    endpoint= "ibge/municipios/v1/",
    query_parameters =  { "providers" : "dados-abertos-br,gov,wikipedia"},
    path_parameters = ['BA', 'CE'],
    download_folder= '../download/'
)
    list_requests = orquestrador.generate_list_query__path_parameters()
    orquestrador.execute_requests_envelope_save_file()

    with open('../creds.json', 'r') as arquivo_json:
        data_json = json.load(arquivo_json)

    connector_postgres = Postgres(
        host='localhost', 
        port=5432, 
        database='postgres', 
        user = data_json['postgres_user'], 
        password = data_json['postgres_password']
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



