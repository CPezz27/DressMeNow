import mysql.connector

from utils import mysql_config
from utils.utils import hash_password

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


def get_all_personale():
    try:
        query = "SELECT * FROM personale"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        return None


def add_personale(email, password, tipo_personale):
    try:
        hashed_password = hash_password(password)
        insert_query = "INSERT INTO personale (email, password, tipo_personale) VALUES (%s, %s, %s)"
        user_data = (email, hashed_password, tipo_personale)
        cursor.execute(insert_query, user_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def view_personale(id_personale):
    search_query = "SELECT * FROM personale WHERE id_personale = %s"
    try:
        cursor.execute(search_query, (id_personale,))
        result = cursor.fetchone()
        if result:
            result_dict = {
                'id_personale': result[0],
                'email': result[1],
                'password': result[2],
                'tipo_personale': result[3]
            }
            return result_dict
        else:
            return None
    except mysql.connector.Error as err:
        return None


def update_personale(id_personale, **kwargs):
    update_query = "UPDATE personale SET "
    update_data = []

    print(kwargs.items())

    for key, value in kwargs.items():
        update_query += f"{key}=%s, "
        update_data.append(value)

    update_query = update_query.rstrip(', ')
    update_query += " WHERE id_personale = %s"
    update_data.append(id_personale)

    try:
        cursor.execute(update_query, update_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def delete_personale(personale_id):
    try:
        delete_query = "DELETE FROM personale WHERE id_personale = %s"
        cursor.execute(delete_query, (personale_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def login(email, password):
    try:
        query = "SELECT * FROM personale WHERE email = %s AND password = %s"

        hashed_password = hash_password(password)

        val = (email, hashed_password)

        cursor.execute(query, val)

        user = cursor.fetchone()

        return user
    except mysql.connector.Error as err:
        return None


class Personale:
    def __init__(self, email, password, tipo_personale):
        self.email = email
        self.password = hash_password(password)
        self.tipo_personale = tipo_personale

    def save(self):
        insert_query = ("INSERT INTO personale "
                        "(email, password, tipo_personale) "
                        "VALUES (%s, %s, %s)")

        # Dati da inserire nel database
        user_data = (self.email, self.password, self.tipo_personale)

        try:
            cursor.execute(insert_query, user_data)

            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
