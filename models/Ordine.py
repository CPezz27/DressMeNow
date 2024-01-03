import mysql.connector

from utils import mysql_config

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


def get_user_orders(user_id):
    try:
        query = ("""
            SELECT o.id_ordine, o.stato AS stato_ordine, o.data AS data_ordine,
                   t.id_transazione, t.data AS data_transazione, t.totale, t.stato AS stato_transazione,
                   p.id_prodotto, p.nome AS nome_prodotto, pio.reso, pio.stato_reso, pio.note_reso
            FROM ordine o
            JOIN transazione t ON o.id_ordine = t.id_ordine
            JOIN prodotto_in_ordine pio ON o.id_ordine = pio.id_ordine
            JOIN prodotto p ON pio.id_prodotto = p.id_prodotto
            WHERE o.id_utente = %s
        """)

        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()

        return orders
    except mysql.connector.Error as err:
        print(f"Errore durante il recupero degli ordini: {err}")
        return []


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
            print("Ordine salvato correttamente nel database.")
        except mysql.connector.Error as err:
            print(f"Errore durante l'inserimento dell'ordine")
