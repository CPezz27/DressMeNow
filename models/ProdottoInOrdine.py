import mysql.connector
from utils.mysql_config import get_database_connection

from utils import mysql_config

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


class ProdottoInOrdine:
    def __init__(self, id_ordine, id_prodotto, reso, stato_reso, note_reso):
        self.id_ordine = id_ordine
        self.id_prodotto = id_prodotto
        self.reso = reso
        self.stato_reso = stato_reso
        self.note_reso = note_reso

    @staticmethod
    def get_products_in_order(order_id):
        conn = get_database_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM prodotto_in_ordine WHERE id_ordine = %s"

        try:
            cursor.execute(query, (order_id,))
            products_in_order = cursor.fetchall()
            return products_in_order
        except mysql.connector.Error as err:
            print(f"Errore durante la lettura dei prodotti in ordine: {err}")
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        insert_query = ("INSERT INTO prodotto_in_ordine "
                        "(id_ordine, id_prodotto, reso, stato_reso, note_reso) "
                        "VALUES (%s, %s, %s, %s, %s)")

        data = (self.id_ordine, self.id_prodotto, self.reso, self.stato_reso, self.note_reso)

        try:
            cursor.execute(insert_query, data)
            conn.commit()
            print("Prodotto in ordine salvato correttamente nel database.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Errore durante l'inserimento del prodotto in ordine: {err}")
        finally:
            cursor.close()
            conn.close()

    def update(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        update_query = ("UPDATE prodotto_in_ordine SET reso = %s, stato_reso = %s, note_reso = %s "
                        "WHERE id_ordine = %s AND id_prodotto = %s")

        data = (self.reso, self.stato_reso, self.note_reso, self.id_ordine, self.id_prodotto)

        try:
            cursor.execute(update_query, data)
            conn.commit()
            print("Prodotto in ordine aggiornato correttamente nel database.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Errore durante l'aggiornamento del prodotto in ordine: {err}")
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        conn = get_database_connection()
        cursor = conn.cursor()
        delete_query = "DELETE FROM prodotto_in_ordine WHERE id_ordine = %s AND id_prodotto = %s"

        try:
            cursor.execute(delete_query, (self.id_ordine, self.id_prodotto))
            conn.commit()
            print("Prodotto in ordine eliminato correttamente dal database.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Errore durante l'eliminazione del prodotto in ordine: {err}")
        finally:
            cursor.close()
            conn.close()

    def conta_prodotti_resi(self):
        try:
            cursor.execute("SELECT COUNT(*) FROM prodotto_in_ordine WHERE reso = 1")
            result = cursor.fetchone()
            if result:
                return result[0]
            return 0
        except mysql.connector.Error as err:
            print(f"Errore durante il conteggio dei prodotti restituiti: {err}")
            return 0

    @staticmethod
    def percentuale_prodotti_resi():
        try:
            cursor.execute("SELECT COUNT(*) FROM prodotto_in_ordine")
            total_products = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM prodotto_in_ordine WHERE reso = 1")
            returned_products = cursor.fetchone()[0]

            if total_products > 0:
                return (returned_products / total_products) * 100
            return 0
        except mysql.connector.Error as err:
            print(f"Errore durante il calcolo della percentuale dei prodotti restituiti: {err}")
            return 0

