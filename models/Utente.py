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
        return None


def get_user(id):
    try:
        query = "SELECT * FROM utente WHERE id_utente = %s"

        cursor.execute(query, (id,))

        user = cursor.fetchone()

        return user
    except mysql.connector.Error as err:
        return None


def get_addresses(id):
    try:
        query = "SELECT * FROM indirizzo WHERE id_utente = %s"

        cursor.execute(query, (id,))

        addresses = cursor.fetchall()

        return addresses
    except mysql.connector.Error as err:
        return None


def delete_account(user_id):
    try:
        conn.start_transaction()

        delete_address_query = "DELETE FROM indirizzo WHERE id_utente = %s"
        cursor.execute(delete_address_query, (user_id,))

        delete_user_query = "DELETE FROM utente WHERE id_utente = %s"
        cursor.execute(delete_user_query, (user_id,))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False


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
        return True
    except mysql.connector.Error as err:
        return False


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
            return True
        except mysql.connector.Error as err:
            return False
