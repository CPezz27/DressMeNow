import base64

import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def aggiungi_al_carrello(id_utente, id_prodotto, size, quantita=1):
    try:
        # Verifica se il carrello dell'utente esiste
        query_get_cart_id = "SELECT id FROM carrello WHERE id_utente = %s"
        cursor.execute(query_get_cart_id, (id_utente,))
        cart_id = cursor.fetchone()

        if cart_id:
            # Verifica se il prodotto è già presente nel carrello
            query_check_product = "SELECT id_prodotto, quantità FROM prodotto_in_carrello WHERE id_carrello = %s AND id_prodotto = %s AND id_taglia = %s"
            cursor.execute(query_check_product, (cart_id[0], id_prodotto, size))
            existing_product = cursor.fetchone()

            if existing_product:
                quantita_esistente = int(existing_product[1])
                quantita = int(quantita)
                nuova_quantita = quantita_esistente + quantita
                query_update_quantity = "UPDATE prodotto_in_carrello SET quantità = %s WHERE id_carrello = %s AND id_prodotto = %s AND id_taglia = %s"
                cursor.execute(query_update_quantity, (nuova_quantita, cart_id[0], id_prodotto, size))
            else:
                # Se il prodotto non è presente, aggiungilo al carrello
                query_insert_product = "INSERT INTO prodotto_in_carrello (id_carrello, id_prodotto, quantità, id_taglia) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_insert_product, (cart_id[0], id_prodotto, quantita, size))

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
            query_check_product = "SELECT quantità FROM prodotto_in_carrello WHERE id_carrello = %s AND id_prodotto = %s"
            cursor.execute(query_check_product, (cart_id[0], id_prodotto))
            existing_quantity = cursor.fetchone()

            if existing_quantity:
                if existing_quantity[0] > 1:
                    query_update_quantity = "UPDATE prodotto_in_carrello SET quantità = quantità - 1 WHERE id_carrello = %s AND id_prodotto = %s"
                    cursor.execute(query_update_quantity, (cart_id[0], id_prodotto))
                else:
                    query_remove_product = "DELETE FROM prodotto_in_carrello WHERE id_carrello = %s AND id_prodotto = %s"
                    cursor.execute(query_remove_product, (cart_id[0], id_prodotto))

                conn.commit()
                return True
            else:
                return False
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
                "GROUP BY pc.id_prodotto, pc.id_taglia, p.nome, p.categoria, p.marca, p.descrizione, p.vestibilità, pc.quantità, "
                "p.prezzo, p.colore, p.materiale"
            )

            cursor.execute(query, (cart_id[0],))
            cart_contents = cursor.fetchall()

            total_price = 0.0

            for item in cart_contents:
                total_price += float(item[9]) * float(item[2])

            total_price = round(total_price, 2)

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
