import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def search_prodotto_by_name(nome):
    search_query = "SELECT * FROM prodotto WHERE nome LIKE %s"
    search_name = f"%{nome}%"

    try:
        cursor.execute(search_query, (search_name,))
        result = cursor.fetchall()

        return result
    except mysql.connector.Error as err:
        print(f"Errore durante la ricerca dei prodotti per nome: {err}")


def view_products():
    search_query = "SELECT * FROM prodotto"

    try:
        cursor.execute(search_query)
        result = cursor.fetchall()

        return result
    except mysql.connector.Error as err:
        print(f"Errore durante la visualizzazione dei prodotti per nome: {err}")


def view_product(product_id):
    search_query = "SELECT * FROM prodotto WHERE id_prodotto = %s"

    try:
        cursor.execute(search_query, (product_id,))
        result = cursor.fetchall()

        return result
    except mysql.connector.Error as err:
        print(f"Errore durante la visualizzazione del prodotto per nome: {err}")


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
        print(f"Prodotto con ID {product_id} aggiornato correttamente.")
    except mysql.connector.Error as err:
        print(f"Errore durante l'aggiornamento del prodotto")


def delete(product_id):
    delete_query = "DELETE FROM prodotto WHERE id_prodotto=%s"

    try:
        cursor.execute(delete_query, (product_id,))

        conn.commit()
        print(f"Prodotto con ID {product_id} eliminato correttamente.")
    except mysql.connector.Error as err:
        print(f"Errore durante l'eliminazione del prodotto")

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
            print("Prodotto salvato correttamente nel database.")
        except mysql.connector.Error as err:
            print(f"Errore durante l'inserimento del prodotto")