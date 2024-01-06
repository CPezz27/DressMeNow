import base64

import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def mostra_info_prodotto():
    try:
        query = (
            "SELECT p.nome, p.prezzo, t.nometaglia, tp.quantita "
            "FROM prodotto p "
            "JOIN taglia_prodotto tp ON p.id_prodotto = tp.id_prodotto "
            "JOIN taglia t ON tp.id_taglia = t.id_taglia"
        )

        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            nome_prodotto = row[0]
            prezzo = row[1]
            taglia = row[2]
            quantita = row[3]
            print(f"{nome_prodotto}, {prezzo}€, {taglia}, {quantita}")

    except mysql.connector.Error as err:
        return False


def search_prodotto_by_name(nome):
    search_query = "SELECT p.*, MIN(i.id_immagine) AS first_image FROM prodotto p LEFT JOIN immagine i ON " \
                   "p.id_prodotto = i.id_prodotto WHERE p.nome LIKE %s GROUP BY p.id_prodotto"
    search_name = f"%{nome}%"

    try:
        cursor.execute(search_query, (search_name,))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        return None


def view_products():
    search_query = "SELECT p.*, MIN(i.id_immagine) AS first_image FROM prodotto p LEFT JOIN immagine i ON " \
                   "p.id_prodotto = i.id_prodotto GROUP BY p.id_prodotto"

    try:
        cursor.execute(search_query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        return None


def view_product(product_id):
    search_query = "SELECT * FROM prodotto WHERE id_prodotto = %s"
    image_query = "SELECT * FROM immagine WHERE id_prodotto = %s"
    size_query = (
        "SELECT t.nometaglia, tp.quantita "
        "FROM taglia t "
        "JOIN taglia_prodotto tp ON t.id_taglia = tp.id_taglia "
        "WHERE tp.id_prodotto = %s"
    )

    try:
        cursor.execute(search_query, (product_id,))
        result = cursor.fetchone()

        cursor.execute(image_query, (product_id,))
        image_result = cursor.fetchall()

        cursor.execute(size_query, (product_id,))
        size_result = cursor.fetchall()

        if result and image_result:
            result_dict = {
                'product_details': result,
                'images': [
                    {'id_immagine': img[0], 'id_prodotto': img[1], 'immagine': base64.b64encode(img[2]).decode('utf-8'),
                     'tipo': img[3]}
                    for img in image_result
                ],
                'sizes': [
                    {'nome_taglia': size[0], 'qta': size[1]}
                    for size in size_result
                ]
            }
            return result_dict
        else:
            return None
    except mysql.connector.Error as err:
        return None


def view_products_by_category(category):
    search_query = "SELECT * FROM prodotto WHERE categoria = %s"

    try:
        cursor.execute(search_query, (category,))
        result = cursor.fetchall()

        return result
    except mysql.connector.Error as err:
        return None


def update_prodotto(product_id, **kwargs):
    update_query = "UPDATE prodotto SET "

    update_data = []
    for key, value in kwargs.items():
        update_query += f"{key}=%s, "
        update_data.append(value)

    update_query = update_query.rstrip(', ')
    update_query += " WHERE id_prodotto=%s"
    update_data.append(product_id)

    try:
        cursor.execute(update_query, update_data)

        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def delete(product_id):
    delete_query = "DELETE FROM prodotto WHERE id_prodotto=%s"

    try:
        cursor.execute(delete_query, (product_id,))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


class Prodotto:
    def __init__(self, nome, categoria, marca, descrizione, vestibilita, prezzo, colore, materiale):
        self.nome = nome
        self.categoria = categoria
        self.marca = marca
        self.descrizione = descrizione
        self.vestibilita = vestibilita
        self.prezzo = prezzo
        self.colore = colore
        self.materiale = materiale

    def save(self):
        insert_query = ("INSERT INTO prodotto "
                        "(nome, categoria, marca, descrizione, vestibilità, prezzo, colore, materiale) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        product_data = (self.nome, self.categoria, self.marca, self.descrizione,
                        self.vestibilita, self.prezzo, self.colore, self.materiale)

        try:
            cursor.execute(insert_query, product_data)

            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
