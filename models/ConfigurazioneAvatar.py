import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def update_configurazione_avatar(id_utente, **kwargs):
    try:
        update_query = "UPDATE configurazione_avatar SET "
        update_data = []

        for key, value in kwargs.items():
            update_query += f"{key}=%s, "
            update_data.append(value)

        update_query = update_query.rstrip(', ')
        update_query += " WHERE id_utente=%s"
        update_data.append(id_utente)

        cursor.execute(update_query, update_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


class ConfigurazioneAvatar:
    def __init__(self, colore_pelle, colore_occhi, colore_capelli, lunghezza_capelli, altezza, peso, barba, eta, dimensioni_corpo, sesso, id_utente):
        self.colore_pelle = colore_pelle
        self.colore_occhi = colore_occhi
        self.colore_capelli = colore_capelli
        self.lunghezza_capelli = lunghezza_capelli
        self.altezza = altezza
        self.peso = peso
        self.barba = barba
        self.eta = eta
        self.dimensioni_corpo = dimensioni_corpo
        self.sesso = sesso
        self.id_utente = id_utente

    def save(self):
        try:
            insert_query = ("INSERT INTO configurazione_avatar "
                            "(colore_pelle, colore_occhi, colore_capelli, lunghezza_capelli, altezza, peso, barba, "
                            "eta, dimensioni_corpo, sesso, id_utente)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            config_data = (self.colore_pelle, self.colore_occhi, self.colore_capelli, self.lunghezza_capelli, self.altezza,
                           self.peso, self.barba, self.eta, self.dimensioni_corpo, self.sesso, self.id_utente)

            cursor.execute(insert_query, config_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
