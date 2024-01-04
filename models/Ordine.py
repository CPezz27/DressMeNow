import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def modifica_ordine(id_ordine, nuovo_stato):
    try:
        update_query = "UPDATE ordine SET stato = %s WHERE id_ordine = %s"
        cursor.execute(update_query, (nuovo_stato, id_ordine))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False


def cancella_ordine(id_ordine):
    try:
        update_query = "UPDATE ordine SET stato = 'cancellato' WHERE id_ordine = %s"
        cursor.execute(update_query, (id_ordine,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False


def modifica_stato_ordine(id_ordine, nuovo_stato):
    try:
        update_query = "UPDATE ordine SET stato = %s WHERE id_ordine = %s"
        cursor.execute(update_query, (nuovo_stato, id_ordine))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False


def calcola_vendite_totali():
    try:
        cursor.execute("SELECT COUNT(*) FROM ordine")
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0
    except mysql.connector.Error as err:
        return None


def calcola_guadagno():
    try:
        cursor.execute("SELECT SUM(totale) FROM transazione")
        result = cursor.fetchone()
        if result and result[0]:
            return result[0]
        return 0
    except mysql.connector.Error as err:
        return None


def get_user_orders(user_id):
    try:
        query = (
            "SELECT o.id_ordine, o.stato AS stato_ordine, o.data AS data_ordine, "
            "t.id_transazione, t.data AS data_transazione, t.totale, t.stato AS stato_transazione, "
            "p.id_prodotto, p.nome AS nome_prodotto, pio.reso, p.prezzo "
            "FROM ordine o "
            "JOIN transazione t ON o.id_ordine = t.id_ordine "
            "JOIN prodotto_in_ordine pio ON o.id_ordine = pio.id_ordine "
            "JOIN prodotto p ON pio.id_prodotto = p.id_prodotto "
            "WHERE o.id_utente = %s "
        )

        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()

        return orders
    except mysql.connector.Error as err:
        return None
    

def modifica_reso(id_prodotto, stato_reso, note_reso, id_ordine):
    update_query = ("UPDATE prodotto_in_ordine "
                    "SET reso = 1, stato_reso = %s, note_reso = %s "
                    "WHERE id_ordine = %s AND id_prodotto = %s")

    reso_data = (stato_reso, note_reso, id_ordine, id_prodotto)

    try:
        cursor.execute(update_query, reso_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


class Ordine:
    def __init__(self, id_utente, stato, data):
        self.id_utente = id_utente
        self.stato = stato
        self.data = data

    def save(self):
        insert_query = ("INSERT INTO ordine "
                        "(id_utente, stato, data) "
                        "VALUES (%s, %s, %s)")

        order_data = (self.id_utente, self.stato, self.data)

        try:
            cursor.execute(insert_query, order_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
    
