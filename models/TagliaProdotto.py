import mysql.connector
from utils import mysql_config
from flask import Blueprint, render_template

conn = mysql_config.get_database_connection()
cursor = conn.cursor()

app_bp = Blueprint('taglia', __name__)

@app_bp.route('/aggiungi_taglia')
def aggiungi_taglia():
    return render_template('aggiungiTaglia.html')


def decrementa_quantita(id_prodotto, id_taglia, quantita_da_decrementare):
    try:
        update_query = ("UPDATE taglia_prodotto "
                        "SET quantita = quantita - %s "
                        "WHERE id_prodotto = %s AND id_taglia = %s")

        cursor.execute(update_query, (quantita_da_decrementare, id_prodotto, id_taglia))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False


class TagliaProdotto:
    def __init__(self, id_taglia, id_prodotto, quantita):
        self.id_taglia = id_taglia
        self.id_prodotto = id_prodotto
        self.quantita = quantita

    def save(self):
        try:
            insert_query = ("INSERT INTO taglia_prodotto "
                            "(id_taglia, id_prodotto, quantita) "
                            "VALUES (%s, %s, %s)")

            taglia_prodotto_data = (self.id_taglia, self.id_prodotto, self.quantita)

            cursor.execute(insert_query, taglia_prodotto_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
