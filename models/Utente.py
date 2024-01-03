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


def delete_account(user_id):
    try:
        conn.start_transaction()

        delete_address_query = "DELETE FROM indirizzo WHERE id_utente = %s"
        cursor.execute(delete_address_query, (user_id,))

        delete_user_query = "DELETE FROM utente WHERE id_utente = %s"
        cursor.execute(delete_user_query, (user_id,))

        conn.commit()
        print("Account eliminato con successo")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Errore durante la cancellazione dell'account: {err}")


def modifica_account(id_utente, **kwargs):
    update_query = "UPDATE utente SET "
    update_values = []

    for campo, valore in kwargs.items()[:-1]:
        update_query += f"{campo} = %s, "
        update_values.append(valore)

    update_query = update_query[:-2] + " WHERE id_utente = %s"
    update_values.append(id_utente)

    try:
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        print("Profilo utente aggiornato correttamente nel database.")
    except mysql.connector.Error as err:
        print(f"Errore durante la modifica del profilo: {err}")


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

        user_data = (self.nome, self.cognome, self.email, self.password,
                     self.sesso, self.numero_telefono, self.data_nascita)

        try:
            cursor.execute(insert_query, user_data)

            conn.commit()
            print("Utente salvato correttamente nel database.")
        except mysql.connector.Error as err:
            print(f"Errore durante l'inserimento dell'utente")

    @classmethod
    def visualizza_tutti_gli_utenti(cls):
        try:
            query = "SELECT * FROM utente"
            cursor.execute(query)

            utenti = cursor.fetchall()

            return utenti
        except mysql.connector.Error as err:
            print(f"Errore durante il recupero degli utenti: {err}")
            return []
        finally:
            cursor.close()
            conn.close()
