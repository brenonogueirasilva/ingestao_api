from Class import BrasilApi
from Class import DirectoryHandler
from Class import Postgres

import os
import pandas as pd
import re

if __name__ == "__main__":
    directory_handler = DirectoryHandler('./download')
    brasil_api =  BrasilApi(
        endpoint= "ibge/municipios/v1/",
        query_parameters = { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameters= ['SP', 'MG' ],
        download_folder= directory_handler.destination_path  
    )
    brasil_api.execute_requests_save_file()