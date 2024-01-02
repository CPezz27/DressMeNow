import mysql.connector

from utils import mysql_config
from utils.utils import hash_password

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


def login(email, password):
    try:
        query = "SELECT * FROM utente WHERE email = %s AND password = %s"

        hashed_password = hash_password(password)

        val = (email, hashed_password)

        cursor.execute(query, val)

        user = cursor.fetchone()

        return user
    except mysql.connector.Error as err:
        print(f"Errore durante l'inserimento dell'utente")


def get_user(id):
    try:
        query = "SELECT * FROM utente WHERE id_utente = %s"

        cursor.execute(query, (id,))

        user = cursor.fetchone()

        return user
    except mysql.connector.Error as err:
        print(f"Errore durante la lettura dell'utente")


def get_addresses(id):
    try:
        query = "SELECT * FROM indirizzo WHERE id_utente = %s"

        cursor.execute(query, (id,))

        addresses = cursor.fetchall()

        return addresses
    except mysql.connector.Error as err:
        print(f"Errore durante la lettura degli indirizzi")


class Utente:
    def __init__(self, nome, cognome, email, password, sesso, numero_telefono, data_nascita):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = hash_password(password)
        self.sesso = sesso
        self.numero_telefono = numero_telefono
        self.data_nascita = data_nascita

    def save(self):
        insert_query = ("INSERT INTO utenti "
                        "(nome, cognome, email, password, sesso, numero_telefono, data_nascita) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        # Dati da inserire nel database
        user_data = (self.nome, self.cognome, self.email, self.password,
                     self.sesso, self.numero_telefono, self.data_nascita)

        try:
            cursor.execute(insert_query, user_data)

            conn.commit()
            print("Utente salvato correttamente nel database.")
        except mysql.connector.Error as err:
            print(f"Errore durante l'inserimento dell'utente")
