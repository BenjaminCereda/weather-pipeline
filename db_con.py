import psycopg
import os 

def get_connection():
    return psycopg.connect(
        host=os.environ["host"],
        dbname=os.environ["dbname"],
        user=os.environ["user"],
        password=os.environ["password"],
        port=os.environ["port"]
    )
