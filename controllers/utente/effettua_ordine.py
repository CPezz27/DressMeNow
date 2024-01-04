from flask import Flask, session, redirect, Blueprint, request
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

        id_prodotto = request.form.get('id_prodotto')
        id_taglia = request.form.get('id_taglia')
        quantita_da_decrementare = 1

        update_query = f"UPDATE taglia_prodotto SET quantita = quantita - {quantita_da_decrementare} " \
                       f"WHERE id_prodotto = {id_prodotto} AND id_taglia = {id_taglia};"

        cursor.execute(update_query)

        return redirect("utente/effettua_ordine")

    except mysql.connector.Error as err:
        return None
