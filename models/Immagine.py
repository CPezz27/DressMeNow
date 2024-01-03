import mysql.connector
from utils.mysql_config import get_database_connection


class Immagine:
    def __init__(self, id_immagine, id_prodotto, immagine, tipo):
        self.id_immagine = id_immagine
        self.id_prodotto = id_prodotto
        self.immagine = immagine
        self.tipo = tipo

    @staticmethod
    def salva_immagine(id_prodotto, immagine, tipo):
        conn = get_database_connection()
        cursor = conn.cursor()

        insert_query = ("INSERT INTO immagine (id_prodotto, immagine, tipo) "
                        "VALUES (%s, %s, %s)")

        try:
            cursor.execute(insert_query, (id_prodotto, immagine, tipo))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def rimuovi_immagine(id_immagine):
        conn = get_database_connection()
        cursor = conn.cursor()

        delete_query = "DELETE FROM immagine WHERE id_immagine = %s"

        try:
            cursor.execute(delete_query, (id_immagine,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
