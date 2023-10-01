import requests
import json
import time
import pandas as pd
import os
from datetime import datetime
import psycopg2
import json 


                    
    
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

