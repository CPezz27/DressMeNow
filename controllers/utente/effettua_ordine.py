from flask import Flask, session, redirect, url_for, Blueprint
from utils import mysql_config
from models import Ordine
from datetime import datetime
import mysql.connector

app = Flask(__name__)

conn = mysql_config.get_database_connection()
cursor = conn.cursor()

app_bp = Blueprint('effettua_ordine', __name__)


@app.route('/effettua_ordine', methods=['POST'])
def effettua_ordine():

    if 'id' not in session:
        return redirect('utente/login')

    try:
        id_utente = session['id']
        stato = "Effettuato"
        data = datetime.now().strftime('%Y-%m-%d')

        nuovo_ordine = Ordine(id_utente, stato, data) #warning che chatGPT non mi sa dire come risolvere
        nuovo_ordine.save()

        return redirect(url_for('riepilogo')) #non esiste ancora

    except mysql.connector.Error as err:
        print(f"Errore durante l'ordine: {err}")
        return redirect(url_for('carrello')) #non esiste ancora

    finally:
        cursor.close()
        conn.close()
