import psycopg2
import pandas as pd

class Postgres:
    '''
    A class for interacting with a PostgreSQL database.

    Parameters:
        - host (str): The hostname or IP address of the PostgreSQL server.
        - port (int): The port number to connect to the PostgreSQL server.
        - database (str): The name of the PostgreSQL database.
        - user (str): The username to use for authentication.
        - password (str): The password for authentication.

    Methods:
        - open_connection():
            Opens a connection to the PostgreSQL database.

        - close_connection():
            Closes the connection to the PostgreSQL database.

        - select(sql_query: str) -> pd.DataFrame:
            Executes a SELECT SQL query and returns the result as a Pandas DataFrame.

        - insert_df(data_frame: pd.DataFrame, table_name: str):
            Inserts data from a Pandas DataFrame into a specified table in the database.

        - create_or_delete_table(sql_query: str):
            Executes a SQL query to create or delete a table in the database.
    '''
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port 
        self.database = database
        self.user = user 
        self.password = password

    def open_connection(self):
        '''
        Opens a connection to the PostgreSQL database.
        '''
        self.conn = psycopg2.connect(
            host= self.host,
            port= self.port,
            database= self.database,
            user = self.user,
            password = self.password
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        '''
        Closes the connection to the PostgreSQL database.
        '''
        self.cursor.close()
        self.conn.close()

    def select(self, sql_query: str) -> pd.DataFrame :
        '''
        Executes a SELECT SQL query and returns the result as a Pandas DataFrame.

        Args:
            sql_query (str): The SELECT SQL query to execute.

        Returns:
            pd.DataFrame: A DataFrame containing the query result.
        '''
        try:
            self.open_connection
            self.cursor.execute(sql_query)
            tabela = self.cursor.fetchall()
            data_frame = pd.DataFrame(tabela, columns=[desc[0] for desc in self.cursor.description])
            return data_frame
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.close_connection()

    def insert_df(self, data_frame: pd.DataFrame, table_name: str):
        '''
        Inserts data from a Pandas DataFrame into a specified table in the database.

        Args:
            data_frame (pd.DataFrame): The DataFrame containing data to insert.
            table_name (str): The name of the table to insert data into.
        '''
        try:
            self.open_connection
            colunas = ', '.join(str(item) for item in list(data_frame.columns))
            for index, row in df.iterrows():
                exec = [row[x] for x in list(data_frame.columns)]
                exec = ', '.join(  "'" + str(item) + "'" if isinstance(item, str) else str(item) for item in exec)
                consulta = f"insert into {table_name} ({colunas}) VALUES ({exec})"
                self.cursor.execute(consulta)
            self.conn.commit()
            print('executado com sucesso')
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.close_connection()
            
    def create_or_delete_table(self, sql_query: str):
        '''
        Executes a SQL query to create or delete a table in the database.

        Args:
            sql_query (str): The SQL query to create or delete a table.
        '''
        try:
            self.open_connection
            self.cursor.execute(sql_query)
            self.conn.commit()
            print('Criacao ou Deleção realizada com sucesso')
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro ao conectar ao PostgreSQL:", error)
        finally:
            self.close_connection()