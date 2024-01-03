import mysql.connector
from utils import mysql_config


import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()



def aggiungi_al_carrello(id_carrello, id_prodotto, quantita=1):
    try:
        query = "INSERT INTO prodotto_in_carrello (id_carrello, id_prodotto, quantita) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_carrello, id_prodotto, quantita))
        conn.commit()
        print("Prodotto aggiunto al carrello con successo.")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Errore durante l'aggiunta del prodotto al carrello: {err}")


def rimuovi_dal_carrello(id_carrello, id_prodotto):
    try:
        query = "DELETE FROM prodotto_in_carrello WHERE id_carrello = %s AND id_prodotto = %s"
        cursor.execute(query, (id_carrello, id_prodotto))
        conn.commit()
        print("Prodotto rimosso dal carrello con successo.")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Errore durante la rimozione del prodotto dal carrello: {err}")


def svuota_carrello(id_carrello):
    try:
        query = "DELETE FROM prodotto_in_carrello WHERE id_carrello = %s"
        cursor.execute(query, (id_carrello,))
        conn.commit()
        print("Carrello svuotato con successo.")
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Errore durante lo svuotamento del carrello: {err}")


def contenuto_carrello(id_carrello):
    try:
        query = "SELECT * FROM prodotto_in_carrello WHERE id_carrello = %s"
        cursor.execute(query, (id_carrello,))
        cart_contents = cursor.fetchall()
        print("Contenuto del carrello:")
        for item in cart_contents:
            print(item)
        return cart_contents
    except mysql.connector.Error as err:
        print(f"Errore durante la visualizzazione del contenuto del carrello: {err}")


class Carrello:
    def __init__(self, id_utente):
        self.id_utente = id_utente
        self.conn = mysql_config.get_database_connection()
        self.cursor = self.conn.cursor()

    def create_cart(self):
        try:
            query = "INSERT INTO carrello (id_utente) VALUES (%s)"
            self.cursor.execute(query, (self.id_utente,))
            self.conn.commit()
            print("Carrello creato con successo.")
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(f"Errore durante la creazione del carrello: {err}")
