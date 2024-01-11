import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


class Transazione:
    def __init__(self, id_utente, id_ordine, data, totale, stato):
        self.id_utente = id_utente
        self.id_ordine = id_ordine
        self.data = data
        self.totale = totale
        self.stato = stato

    def save(self):
        insert_query = ("INSERT INTO transazione "
                        "(id_utente, id_ordine, data, totale, stato) "
                        "VALUES (%s, %s, %s, %s, %s)")

        order_data = (self.id_utente, self.id_ordine, self.data, self.totale, self.stato)

        try:
            cursor.execute(insert_query, order_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False

