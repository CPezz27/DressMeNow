import base64

import mysql.connector
import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def aggiungi_al_carrello(id_utente, id_prodotto, quantita=1):
    try:
        query_get_cart_id = "SELECT id FROM carrello WHERE id_utente = %s"
        cursor.execute(query_get_cart_id, (id_utente,))
        cart_id = cursor.fetchone()

        if cart_id:
            query = "INSERT INTO prodotto_in_carrello (id_carrello, id_prodotto, quantità) VALUES (%s, %s, %s)"
            cursor.execute(query, (cart_id[0], id_prodotto, quantita))
            conn.commit()
            return True
        else:
            return False
    except mysql.connector.Error as err:
        return False


def rimuovi_dal_carrello(id_utente, id_prodotto):
    try:
        query_get_cart_id = "SELECT id FROM carrello WHERE id_utente = %s"
        cursor.execute(query_get_cart_id, (id_utente,))
        cart_id = cursor.fetchone()

        if cart_id:
            query = "DELETE FROM prodotto_in_carrello WHERE id_carrello = %s AND id_prodotto = %s"
            cursor.execute(query, (cart_id[0], id_prodotto))
            conn.commit()
            return True
        else:
            return False
    except mysql.connector.Error as err:
        return False


def svuota_carrello(id_utente):
    try:
        query_get_cart_id = "SELECT id FROM carrello WHERE id_utente = %s"
        cursor.execute(query_get_cart_id, (id_utente,))
        cart_id = cursor.fetchone()

        if cart_id:
            query = "DELETE FROM prodotto_in_carrello WHERE id_carrello = %s"
            cursor.execute(query, (cart_id[0],))
            conn.commit()
            return True
        else:
            return False
    except mysql.connector.Error as err:
        return False


def contenuto_carrello(id_utente):
    try:
        query_get_cart_id = "SELECT id FROM carrello WHERE id_utente = %s"
        cursor.execute(query_get_cart_id, (id_utente,))
        cart_id = cursor.fetchone()

        if cart_id:
            query = (
                "SELECT pc.*, p.nome, p.categoria, p.marca, p.descrizione, p.vestibilità, "
                "p.prezzo, p.colore, p.materiale, TO_BASE64(MAX(i.immagine)) as immagine "
                "FROM prodotto_in_carrello pc "
                "JOIN prodotto p ON pc.id_prodotto = p.id_prodotto "
                "LEFT JOIN (SELECT id_prodotto, immagine FROM immagine WHERE tipo = 'pagina_prodotto') i "
                "ON pc.id_prodotto = i.id_prodotto "
                "WHERE pc.id_carrello = %s "
                "GROUP BY pc.id_prodotto, p.nome, p.categoria, p.marca, p.descrizione, p.vestibilità, pc.quantità, "
                "p.prezzo, p.colore, p.materiale"
            )

            cursor.execute(query, (cart_id[0],))
            cart_contents = cursor.fetchall()

            query_total_price = (
                "SELECT SUM(p.prezzo) as totale_prezzo "
                "FROM prodotto_in_carrello pc "
                "JOIN prodotto p ON pc.id_prodotto = p.id_prodotto "
                "WHERE pc.id_carrello = %s"
            )
            cursor.execute(query_total_price, (cart_id[0],))
            total_price = cursor.fetchone()[0]

            return cart_contents, total_price
        else:
            return None, None
    except mysql.connector.Error as err:
        return None, None


class Carrello:
    def __init__(self, id_utente):
        self.id_utente = id_utente
        self.conn = mysql_config.get_database_connection()
        self.cursor = self.conn.cursor()

    def save(self):
        try:
            query = "INSERT INTO carrello (id_utente) VALUES (%s)"
            self.cursor.execute(query, (self.id_utente,))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            return False
