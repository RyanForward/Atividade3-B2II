
import psycopg2
from importlib.metadata import version

def connect():
    try:
        northwind = psycopg2.connect(
            host='localhost',
            dbname='northwind', 
            user = 'postgres', 
            password = 'root'
        )
        print ("Conexão executada com sucesso")
        return northwind
    except OperationalError as e:
        print(e)