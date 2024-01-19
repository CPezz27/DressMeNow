import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


def get_products_in_order(order_id):
    query = "SELECT * FROM prodotto_in_ordine WHERE id_ordine = %s"

    try:
        cursor.execute(query, (order_id,))
        products_in_order = cursor.fetchall()
        return products_in_order
    except mysql.connector.Error as err:
        return None


class ProdottoInOrdine:
    def __init__(self, id_ordine, id_prodotto, id_taglia, quantita, reso, stato_reso, note_reso):
        self.id_ordine = id_ordine
        self.id_prodotto = id_prodotto
        self.id_taglia = id_taglia
        self.quantita = quantita
        self.reso = reso
        self.stato_reso = stato_reso
        self.note_reso = note_reso

    def save(self):
        insert_query = ("INSERT INTO prodotto_in_ordine "
                        "(id_ordine, id_prodotto, id_taglia, quantita, reso, stato_reso, note_reso) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        data = (self.id_ordine, self.id_prodotto, self.id_taglia, self.quantita, self.reso, self.stato_reso, self.note_reso)

        try:
            cursor.execute(insert_query, data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False

    def update(self):
        update_query = ("UPDATE prodotto_in_ordine SET reso = %s, stato_reso = %s, note_reso = %s "
                        "WHERE id_ordine = %s AND id_prodotto = %s")

        data = (self.reso, self.stato_reso, self.note_reso, self.id_ordine, self.id_prodotto)

        try:
            cursor.execute(update_query, data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False

    def delete(self):
        delete_query = "DELETE FROM prodotto_in_ordine WHERE id_ordine = %s AND id_prodotto = %s"

        try:
            cursor.execute(delete_query, (self.id_ordine, self.id_prodotto))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
