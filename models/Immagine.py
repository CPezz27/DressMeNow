import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def salva_immagine(id_prodotto, immagine, tipo):
    nuova_immagine = Immagine(None, id_prodotto, immagine, tipo)
    return nuova_immagine.save()


def rimuovi_immagine(id_immagine):

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


class Immagine:
    def __init__(self, id_immagine, id_prodotto, immagine, tipo):
        self.id_immagine = id_immagine
        self.id_prodotto = id_prodotto
        self.immagine = immagine
        self.tipo = tipo

    def save(self):

        insert_query = ("INSERT INTO immagine (id_prodotto, immagine, tipo) "
                        "VALUES (%s, %s, %s)")

        try:
            cursor.execute(insert_query, (self.id_prodotto, self.immagine, self.tipo))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
