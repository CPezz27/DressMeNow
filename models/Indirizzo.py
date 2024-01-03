import mysql.connector
from utils.mysql_config import get_database_connection


def get_addresses(id_utente):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM indirizzo WHERE id_utente = %s"

    try:
        cursor.execute(query, (id_utente,))
        addresses = cursor.fetchall()
        return addresses
    except mysql.connector.Error as err:
        return None
    finally:
        cursor.close()
        conn.close()


class Indirizzo:
    def __init__(self, provincia, cap, via, tipo, citta):
        self.provincia = provincia
        self.cap = cap
        self.via = via
        self.tipo = tipo
        self.citta = citta

    def save(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        insert_query = ("INSERT INTO indirizzo "
                        "(id_utente, provincia, cap, via, tipo, città) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")

        data = (self.provincia, self.cap, self.via, self.tipo, self.citta)

        try:
            cursor.execute(insert_query, data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        update_query = ("UPDATE indirizzo SET provincia = %s, cap = %s, via = %s, tipo = %s, città = %s "
                        "WHERE id_indirizzo = %s")

        data = (self.provincia, self.cap, self.via, self.tipo, self.citta)

        try:
            cursor.execute(update_query, data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        delete_query = "DELETE FROM indirizzo WHERE id_indirizzo = %s"

        try:
            cursor.execute(delete_query, self)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
