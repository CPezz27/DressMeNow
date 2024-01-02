import mysql.connector

from utils import mysql_config

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


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
