import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def aggiungi_taglia(nome_taglia):
    try:
        insert_query = "INSERT INTO taglia (nometaglia) VALUES (%s)"
        taglia_data = (nome_taglia,)

        cursor.execute(insert_query, taglia_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def modifica_taglia(id_taglia, nome_taglia):
    try:
        update_query = "UPDATE taglia SET nometaglia = %s WHERE id_taglia = %s"
        taglia_data = (nome_taglia, id_taglia)
        cursor.execute(update_query, taglia_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


def rimozione_taglia(id_taglia):
    delete_query = "DELETE FROM taglia WHERE id_taglia = %s"

    try:
        cursor.execute(delete_query, (id_taglia,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False


def get_taglia_by_id(id_taglia):
    select_query = "SELECT id_taglia, nometaglia FROM taglia WHERE id_taglia = %s"
    cursor.execute(select_query, (id_taglia,))
    result = cursor.fetchone()

    if result:
        id_taglia, nome_taglia = result
        return id_taglia, nome_taglia
    else:
        return None
    
def inserisci_taglia_prodotto_nel_database(id_taglia, id_prodotto, quantita):
    insert_query = ("INSERT INTO taglia_prodotto "
                        "(id_taglia, id_prodotto, quantita) "
                        "VALUES (%s, %s, %s)")

    product_data = (id_taglia, id_prodotto, quantita)

    try:
        cursor.execute(insert_query, product_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False

    
    
def get_taglie_quantita_by_id_prodotto(id_prodotto):
    #select_query ="SELECT taglia.id_taglia, taglia.nome_taglia, taglia_prodotto.quantita FROM taglia_prodotto INNER JOIN taglia ON taglia_prodotto.id_taglia = taglia.id_taglia WHERE taglia_prodotto.id_prodotto = %s"
    select_query = """
        SELECT taglia.id_taglia, taglia.nometaglia, taglia_prodotto.quantita 
        FROM taglia_prodotto 
        INNER JOIN taglia ON taglia_prodotto.id_taglia = taglia.id_taglia 
        WHERE taglia_prodotto.id_prodotto = %s
    """

    cursor.execute(select_query, (id_prodotto,))
    results = cursor.fetchall()

    taglie_quantita = []
    for row in results:
        id_taglia, nome_taglia, quantita = row
        taglie_quantita.append({
            'id_taglia': id_taglia,
            'nome_taglia': nome_taglia,
            'quantita': quantita
        })

    return taglie_quantita


def get_elenco_taglie():
    select_query = "SELECT id_taglia, nometaglia FROM taglia"
    cursor.execute(select_query)
    results = cursor.fetchall()

    elenco_taglie = []
    for result in results:
        id_taglia, nome_taglia = result
        elenco_taglie.append((id_taglia, nome_taglia))

    return elenco_taglie


class Taglia:   #raffinato il carico
    def __init__(self, id_taglia=None, nome_taglia=None):
        self.id_taglia = id_taglia
        self.nome_taglia = nome_taglia

    def save(self):
        if self.id_taglia:
            success = modifica_taglia(self.id_taglia, self.nome_taglia)
        else:
            success = aggiungi_taglia(self.nome_taglia)

        return success
