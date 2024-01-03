import mysql.connector

from utils import mysql_config
from utils.utils import hash_password

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


def login(email, password):
    try:
        query = "SELECT * FROM personale WHERE email = %s AND password = %s"

        hashed_password = hash_password(password)

        val = (email, hashed_password)

        cursor.execute(query, val)

        user = cursor.fetchone()

        return user
    except mysql.connector.Error as err:
        return False


class Direttore:
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
