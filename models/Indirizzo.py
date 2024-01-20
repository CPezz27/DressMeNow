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
    def __init__(self, id_utente, provincia, cap, via, tipo, città):
        self.id_utente = id_utente
        self.provincia = provincia
        self.cap = cap
        self.via = via
        self.tipo = tipo
        self.città = città

    def save(self):
        count_query = ("SELECT COUNT(*) FROM indirizzo WHERE id_utente = %s")
        cursor.execute(count_query, (self.id_utente,))
        count_result = cursor.fetchone()[0]

        if count_result >= 2:
            return False, "Errore, il numero massimo di indirizzi è già stato raggiunto"

        check_query = ("SELECT COUNT(*) FROM indirizzo WHERE id_utente = %s AND tipo = %s")
        cursor.execute(check_query, (self.id_utente, self.tipo))
        check_result = cursor.fetchone()[0]

        if check_result > 0:
            msg = "Errore, è già presente un indirizzo di " + self.tipo
            return False, msg

        insert_query = ("INSERT INTO indirizzo (id_utente, provincia, cap, via, tipo, città) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")

        try:
            cursor.execute(insert_query, (self.id_utente, self.provincia, self.cap, self.via, self.tipo, self.città))
            conn.commit()
            return True, "Inserimento avvenuto con successo"
        except mysql.connector.Error as err:
            return False, str(err)
