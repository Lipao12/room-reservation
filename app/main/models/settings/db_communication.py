import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection 
from dotenv import load_dotenv
import os

load_dotenv()

class DbConnectionHandler:
    def __init__(self)->None:
        load_dotenv()
        self.database_url = os.getenv('DATABASE_URL')
        #self.user = os.getenv('USER')
        #self.password = os.getenv('PASSWORD')
        #self.host = os.getenv('HOST')
        #self.port = os.getenv('PORT')
        #self.database = os.getenv('DATABASE')
        self.__conn = None
    
    def connect(self)->None:
        try:
            '''elf.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )'''
            self.connection = psycopg2.connect(self.database_url)
            print("Conexão com o PostgreSQL foi estabelecida com sucesso.")
        except OperationalError as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
    def get_connection(self):
        if self.__conn is None:
            self.connect()
        return self.connection

db_connection_handler = DbConnectionHandler()