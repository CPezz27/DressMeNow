import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()



def conta_ordini_resi():
    try:
        cursor.execute("SELECT COUNT(*) FROM ordine WHERE reso = 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0
    except mysql.connector.Error as err:
        return None


def percentuale_ordini_resi():
    try:
        cursor.execute("SELECT COUNT(*) FROM ordine")
        total_products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ordine WHERE reso = 1")
        returned_products = cursor.fetchone()[0]

        if total_products > 0:
            return (returned_products / total_products) * 100
        return 0
    except mysql.connector.Error as err:
        return None



def modifica_ordine(id_ordine, nuovo_stato):
    try:
        update_query = "UPDATE ordine SET stato = %s WHERE id_ordine = %s"
        cursor.execute(update_query, (nuovo_stato, id_ordine))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def cancella_ordine(id_ordine):
    try:
        update_query = "UPDATE ordine SET stato = 'cancellato' WHERE id_ordine = %s"
        cursor.execute(update_query, (id_ordine,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def modifica_stato_ordine(id_ordine, nuovo_stato):
    try:
        update_query = "UPDATE ordine SET stato = %s WHERE id_ordine = %s"
        cursor.execute(update_query, (nuovo_stato, id_ordine))
        conn.commit()
        return True
    except mysql.connector.Error as err:
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


def visualizza_ordine(order_id):
        query = (
            "SELECT o.id_ordine, o.stato AS stato_ordine, o.data AS data_ordine, t.id_transazione, t.data AS data_transazione, t.totale, t.stato AS stato_transazione, p.id_prodotto, p.nome AS nome_prodotto, o.reso, p.prezzo, iu.id_utente AS id_utente, iu.nome AS nome_utente, iu.cognome AS cognome_utente, iu.email AS email_utente, iu.telefono, i.id_indirizzo, i.provincia AS provincia_indirizzo, i.cap AS cap_indirizzo, i.via AS via_indirizzo, i.tipo AS tipo_indirizzo, i.città AS città_indirizzo, p.marca, o.note_reso, o.reso FROM ordine o JOIN transazione t ON o.id_ordine = t.id_ordine JOIN prodotto_in_ordine pio ON o.id_ordine = pio.id_ordine JOIN prodotto p ON pio.id_prodotto = p.id_prodotto JOIN utente iu ON o.id_utente = iu.id_utente JOIN indirizzo i ON iu.id_utente = i.id_utente WHERE o.id_ordine = %s AND i.tipo = 'Spedizione';"
        )

        cursor.execute(query, (order_id,))
        order_details = cursor.fetchall()

        if order_details:

            order_dict = {
                'id_ordine': order_details[0][0],
                'stato_ordine': order_details[0][1],
                'data_ordine': order_details[0][2],
                'id_transazione': order_details[0][3],
                'data_transazione': order_details[0][4],
                'totale': order_details[0][5],
                'stato_transazione': order_details[0][6],
                'note_reso': order_details[0][23],
                'flag_reso': order_details[0][24],
                'utente': {
                    'id_utente': order_details[0][11],  # Modificato l'indice per l'id_utente
                    'nome_utente': order_details[0][12],  # Modificato l'indice per il nome_utente
                    'cognome_utente': order_details[0][13],  # Modificato l'indice per il cognome_utente
                    'email_utente': order_details[0][14],  # Modificato l'indice per l'email_utente
                    'telefono_utente': order_details[0][15]  # Modificato l'indice per il telefono_utente
                },
                'indirizzo': {
                    'id_indirizzo': order_details[0][16],  # Modificato l'indice per l'id_indirizzo
                    'provincia_indirizzo': order_details[0][17],  # Modificato l'indice per la provincia_indirizzo
                    'cap_indirizzo': order_details[0][18],  # Modificato l'indice per il cap_indirizzo
                    'via_indirizzo': order_details[0][19],  # Modificato l'indice per la via_indirizzo
                    'tipo_indirizzo': order_details[0][20],  # Modificato l'indice per il tipo_indirizzo
                    'città_indirizzo': order_details[0][21]  # Modificato l'indice per la città_indirizzo
                },
                'prodotti': []
            }

            for row in order_details:
                product = {
                    'id_prodotto': row[7],
                    'nome_prodotto': row[8],
                    'reso': row[9],
                    'prezzo': row[10],
                    'marca': row[18]
                }
                order_dict['prodotti'].append(product)
            
            return order_dict
        else:
            return None


def visualizza_ordine_conimg(order_id):
    query = (
        "SELECT o.id_ordine, o.stato AS stato_ordine, o.data AS data_ordine, t.id_transazione, t.data AS data_transazione, t.totale, t.stato AS stato_transazione, "
        "pio.quantita, p.id_prodotto, p.nome AS nome_prodotto, o.reso, p.prezzo, p.materiale, iu.id_utente AS id_utente, iu.nome AS nome_utente, iu.cognome AS cognome_utente, "
        "iu.email AS email_utente, iu.telefono, p.marca, (SELECT TO_BASE64(immagine) FROM immagine i WHERE i.id_prodotto = p.id_prodotto AND i.tipo = 'pagina_prodotto' LIMIT 1), o.note_reso "
        "FROM ordine o "
        "JOIN transazione t ON o.id_ordine = t.id_ordine "
        "JOIN prodotto_in_ordine pio ON o.id_ordine = pio.id_ordine "
        "JOIN prodotto p ON pio.id_prodotto = p.id_prodotto "
        "JOIN utente iu ON o.id_utente = iu.id_utente "
        "WHERE o.id_ordine = %s;"
    )

    cursor.execute(query, (order_id,))
    order_details = cursor.fetchall()

    if order_details:
        order_dict = {
            'id_ordine': order_details[0][0],
            'stato_ordine': order_details[0][1],
            'data_ordine': order_details[0][2],
            'id_transazione': order_details[0][3],
            'data_transazione': order_details[0][4],
            'totale': order_details[0][5],
            'stato_transazione': order_details[0][6],
            'reso_ordine': order_details[0][10],
            'note_reso': order_details[0][20],
            'utente': {
                'id_utente': order_details[0][13],  # Modificato l'indice per l'id_utente
                'nome_utente': order_details[0][14],  # Modificato l'indice per il nome_utente
                'cognome_utente': order_details[0][15],  # Modificato l'indice per il cognome_utente
                'email_utente': order_details[0][16],  # Modificato l'indice per l'email_utente
                'telefono_utente': order_details[0][17]  # Modificato l'indice per il telefono_utente
            },
            'prodotti': []
        }

        for row in order_details:
            product = {
                'id_prodotto': row[8],
                'nome_prodotto': row[9],
                'reso': row[10],
                'prezzo': row[11],
                'materiale': row[12],
                'quantita': row[7],
                'marca': row[18],
                'immagine': row[19]  # Aggiunto l'indice per l'immagine
            }
            order_dict['prodotti'].append(product)

        return order_dict
    else:
        return None


def get_user_orders(user_id):
    try:
        query = (
            "SELECT o.id_ordine, o.stato AS stato_ordine, o.data AS data_ordine, "
            "t.id_transazione, t.data AS data_transazione, t.totale, t.stato AS stato_transazione, "
            "p.id_prodotto, p.nome AS nome_prodotto, o.reso, p.prezzo "
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
    

def modifica_reso(stato, note_reso, id_ordine):
    update_query = ("UPDATE ordine "
                    "SET reso = 1, stato = %s, note_reso = %s "
                    "WHERE id_ordine = %s")

    reso_data = (stato, note_reso, id_ordine)

    try:
        cursor.execute(update_query, reso_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def get_all_orders_with_details():
        try:
            query = (
                "SELECT DISTINCT o.id_ordine, u.email AS email_utente, o.stato AS stato_ordine, o.data AS data_ordine FROM ordine o JOIN utente u ON o.id_utente = u.id_utente ORDER BY o.id_ordine;"
            )

            cursor.execute(query)
            orders_details = cursor.fetchall()

            return orders_details
        except mysql.connector.Error as err:
            return None


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
            return cursor.lastrowid
        except mysql.connector.Error as err:
            return None
    
