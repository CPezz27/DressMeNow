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


def get_all_users():
    try:
        query = "SELECT * FROM utente"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
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
        soft_delete_user_query = "UPDATE utente SET is_deleted = 1 WHERE id_utente = %s"
        cursor.execute(soft_delete_user_query, (user_id,))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def modifica_account(id_utente, **kwargs):
    update_query = "UPDATE utente SET "
    update_values = []

    kwargs.pop('is_deleted', None)

    items = list(kwargs.items())

    print(items)

    for index, (campo, valore) in enumerate(items):
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


def view_utente(id_utente):
    search_query = "SELECT * FROM utente WHERE id_utente = %s"
    try:
        cursor.execute(search_query, (id_utente,))
        result = cursor.fetchone()
        if result:
            result_dict = {
                'id_utente': result[0],
                'nome': result[1],
                'cognome': result[2],
                'email': result[3],
                'password': result[4],
                'data_nascita': result[5],
                'telefono': result[6],
                'sesso': result[7],
                'is_deleted': result[8]
            }
            return result_dict
        else:
            return None
    except mysql.connector.Error as err:
        return None


def update_utente(id_utente, **kwargs):
    update_query = "UPDATE utente SET "
    update_data = []

    for key, value in kwargs.items():
        update_query += f"{key}=%s, "
        update_data.append(value)

    update_query = update_query.rstrip(', ')
    update_query += " WHERE id_utente = %s"
    update_data.append(id_utente)

    try:
        cursor.execute(update_query, update_data)
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
        try:
            conn.start_transaction()

            insert_user_query = ("INSERT INTO utente "
                                "(nome, cognome, email, password, sesso, telefono, data_nascita) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)")

            user_data = (self.nome, self.cognome, self.email, self.password,
                         self.sesso, self.numero_telefono, self.data_nascita)

            cursor.execute(insert_user_query, user_data)

            user_id = cursor.lastrowid

            insert_cart_query = "INSERT INTO carrello (id_utente) VALUES (%s)"
            cursor.execute(insert_cart_query, (user_id,))

            insert_avatar_query = ("INSERT INTO configurazione_avatar "
                                  "(colore_pelle, colore_occhi, colore_capelli, lunghezza_capelli, "
                                  "altezza, peso, barba, eta, dimensioni_corpo, sesso, id_utente) "
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            avatar_data = ("rosa pallido", "marrone", "nero", "9", 170, 163, 0, 25, "normale", self.sesso, user_id)

            cursor.execute(insert_avatar_query, avatar_data)

            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
