import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_database_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USERNAME'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )
        print("Connessione al database avvenuta con successo.")
        return conn
    except mysql.connector.Error as err:
        print(f"Errore durante la connessione al database: {err}")
        return None
