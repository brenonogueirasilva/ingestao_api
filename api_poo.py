import requests
import json
import time
import pandas as pd
import os
from datetime import datetime
import psycopg2
import json 

class BrasilApi:
    def __init__(self, endpoint, token = None, parameters ):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.token  = token
        self.parameters = parameters 
        self.requisicoes = 0
        self.limite_requisicoes = 3

    def request(self, par_pagina, par_orgao):
        parametros = {
            "mesAnoFim" : self.par_mes_ano_fim,
            "mesAnoInicio" : self.par_mes_ano_inicio,
            "pagina" : par_pagina,
            "uf" : self.par_uf,
            "orgaoSuperior" : par_orgao
        }
        header = {
            "chave-api-dados" : self.token
        }
        response = requests.get(self.url, params=parametros, headers= header)
        return response
    
    def save_json(self, nome_arquivo, data):
        path_save = f'{self.download_folder}{nome_arquivo}.json'
        data = data.json()
        with open(path_save, 'w') as json_file:
            json.dump(data, json_file, indent=4) 

    def execute_requests_save_json(self):
        resposta = None
        #loop para os orgaos
        for orgao in self.par_orgao_superior:
            cond = True
            pagina = 0
            # loop da pagina
            while cond:
                pagina += 1
                nome_documento = f"recursos_pag({pagina})_orgao({orgao})"
                resposta = self.request(pagina, orgao)
                self.requisicoes += 1
                if self.requisicoes >= self.limite_requisicoes:
                    print('limite de requisicoes atingido por minutos, aguardando')
                    time.sleep(2)
                    self.requisicoes = 0
                if len(resposta.content) > 2:
                    self.save_json(nome_documento, resposta)
                else:
                    cond = False
                    
    def json_to_df(self):
        ls_dfs = []
        for nome_arquivo in os.listdir(self.download_folder):
            df = pd.read_json(self.download_folder + nome_arquivo)
            ls_dfs.append(df)
        df_union = pd.concat(ls_dfs)
        return df_union
    
class Postgres:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port 
        self.database = database
        self.user = user 
        self.password = password

    def conexao(self):
        self.conn = psycopg2.connect(
            host= self.host,
            port= self.port,
            database= self.database,
            user = self.user,
            password = self.password
        )
        self.cursor = self.conn.cursor()

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()

    def select(self, sql):
        try:
            self.conexao()
            self.cursor.execute(sql)
            tabela = self.cursor.fetchall()
            df = pd.DataFrame(tabela, columns=[desc[0] for desc in self.cursor.description])
            return df
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.fechar_conexao()

    def insert_df(self, df, tabela):
        try:
            self.conexao()
            colunas = ', '.join(str(item) for item in list(df.columns))
            for index, row in df.iterrows():
                exec = [row[x] for x in list(df.columns)]
                exec = ', '.join(  "'" + str(item) + "'" if isinstance(item, str) else str(item) for item in exec)
                consulta = f"insert into {tabela} ({colunas}) VALUES ({exec})"
                self.cursor.execute(consulta)
            self.conn.commit()
            print('executado com sucesso')
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.fechar_conexao()
            
    def create_or_delete_table(self, sql):
        try:
            self.conexao()
            self.cursor.execute(sql)
            self.conn.commit()
            print('Criacao ou Deleção realizada com sucesso')
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.fechar_conexao()

if __name__ == "__main__":
    with open('./creds.json', 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)

    api_recurso = Api(
        url= "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos", 
        download_folder='./downloads/',
        token= dados_json['token'],
        par_mes_ano_inicio="01/2023",
        par_mes_ano_fim="01/2023",
        par_orgao_superior= [ 41000,  42000 ] ,
        par_uf= "SP"
    )
    api_recurso.execute_requests_save_json()
    df = api_recurso.json_to_df()

    conexao_postgres = Postgres(host='localhost', port=5432, database='postgres', user = dados_json['postgres_user'], password = dados_json['postgres_password']) 
    sql_insert = '''
    CREATE TABLE IF NOT EXISTS public.recursos (
        anoMes INT,
        codigoPessoa VARCHAR(255),
        nomePessoa VARCHAR(255),
        tipoPessoa VARCHAR(255),
        municipioPessoa VARCHAR(255),
        siglaUFPessoa VARCHAR(255),
        codigoUG INT,
        nomeUG VARCHAR(255),
        codigoOrgao INT,
        nomeOrgao VARCHAR(255),
        codigoOrgaoSuperior INT,
        nomeOrgaoSuperior VARCHAR(255),
        valor NUMERIC(10, 2),
        data_exec TIMESTAMP
    );
    '''
    conexao_postgres.create_or_delete_table(sql_insert)
    # conexao_postgres.create_or_delete_table("delete from public.recursos")
    conexao_postgres.insert_df(df, 'public.recursos')
    conexao_postgres.select("select * from public.recursos")

