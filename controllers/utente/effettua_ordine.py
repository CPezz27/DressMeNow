from flask import Flask, session, redirect, Blueprint
from models.Ordine import Ordine
from datetime import datetime
import mysql.connector

app = Flask(__name__)

app_bp = Blueprint('effettua_ordine', __name__)


@app.route('/effettua_ordine', methods=['POST'])
def effettua_ordine():

    if 'id' not in session:
        return redirect('utente/login')

    try:
        id_utente = session['id']
        stato = "Effettuato"
        data = datetime.now().strftime('%Y-%m-%d')

        nuovo_ordine = Ordine(
                    id_utente=id_utente,
                    stato=stato,
                    data=data)

        nuovo_ordine.save()

        return redirect("utente/effettua_ordine")

    except mysql.connector.Error as err:
        print(f"Errore durante l'ordine: {err}")
        return redirect("utente/carrello")
