import mysql.connector
from utils import mysql_config
from io import BytesIO

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def visualizza_immagini():
    query = "SELECT id_immagine, id_prodotto, TO_BASE64(immagine) as immagine, tipo FROM immagine"
    try:
        cursor.execute(query)
        immagini = cursor.fetchall()
        return immagini
    except mysql.connector.Error as err:
        return None
    

def visualizza_immagini_prodotto(id_prodotto):
    query = "SELECT id_immagine, id_prodotto, TO_BASE64(immagine) as immagine, tipo FROM immagine WHERE id_prodotto=%s"
    try:
        cursor.execute(query, (id_prodotto,))
        immagini = cursor.fetchall()
        return immagini
    except mysql.connector.Error as err:
        return None


def rimuovi_immagine(id_immagine):
    delete_query = "DELETE FROM immagine WHERE id_immagine = %s"
    try:
        cursor.execute(delete_query, (id_immagine,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        cursor.close()
        conn.close()


class Immagine:
    def __init__(self, id_prodotto, immagine, tipo):
        self.id_prodotto = id_prodotto
        self.immagine = immagine
        self.tipo = tipo

    def save(self):

        insert_query = ("INSERT INTO immagine (id_prodotto, immagine, tipo) "
                        "VALUES (%s, %s, %s)")

        try:
            image_bytes = BytesIO(self.immagine.read()).getvalue()
            cursor.execute(insert_query, (self.id_prodotto, image_bytes, self.tipo))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
        finally:
            cursor.close()
            conn.close()
