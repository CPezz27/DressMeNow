import mysql.connector
from utils import mysql_config


conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def get_address(address_id):
    query = "SELECT * FROM indirizzo WHERE id_indirizzo = %s"

    try:
        cursor.execute(query, (address_id,))
        address = cursor.fetchone()
        return address
    except mysql.connector.Error as err:
        return None


def get_addresses(id_utente):
    query = "SELECT * FROM indirizzo WHERE id_utente = %s"

    try:
        cursor.execute(query, (id_utente,))
        addresses = cursor.fetchall()
        print(str(addresses))
        return addresses
    except mysql.connector.Error as err:
        return None


def update(provincia, cap, via, tipo, citta, id_indirizzo):
    update_query = ("UPDATE indirizzo SET provincia = %s, cap = %s, via = %s, tipo = %s, città = %s "
                    "WHERE id_indirizzo = %s")

    data = (provincia, cap, via, tipo, citta, id_indirizzo)

    try:
        cursor.execute(update_query, data)
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        return False


def delete(id_indirizzo):
    delete_query = "DELETE FROM indirizzo WHERE id_indirizzo = %s"

    try:
        cursor.execute(delete_query, (id_indirizzo,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


class Indirizzo:
    def __init__(self, id_utente, provincia, cap, via, tipo, citta):
        self.id_utente = id_utente
        self.provincia = provincia
        self.cap = cap
        self.via = via
        self.tipo = tipo
        self.citta = citta

    def save(self):
        insert_query = ("INSERT INTO indirizzo "
                        "(id_utente, provincia, cap, via, tipo, città) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")

        data = (self.id_utente, self.provincia, self.cap, self.via, self.tipo, self.citta)

        try:
            cursor.execute(insert_query, data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
