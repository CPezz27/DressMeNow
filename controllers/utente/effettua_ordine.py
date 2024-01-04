from flask import Flask, session, redirect, Blueprint, request, url_for
from models.Ordine import Ordine
from models import TagliaProdotto
from datetime import datetime
import mysql.connector
#da modificare tutto il controller


app = Flask(__name__)

app_bp = Blueprint('effettua_ordine', __name__)


@app.route('/effettua_ordine', methods=['POST'])
def effettua_ordine():
    if request.method == 'POST':
        try:
            if 'logged_in' not in session or not session['logged_in']:
                return redirect(url_for('user_login.login_page'))

            id_utente = session['id']
            id_prodotto = request.form.get('id_prodotto')
            id_taglia = request.form.get('id_taglia')
            quantita_da_decrementare = 1
            data = datetime.now().strftime('%Y-%m-%d')

            nuovo_ordine = Ordine(
                        id_utente=id_utente,
                        stato="Effettuato",
                        data=data)

            nuovo_ordine.save()

            TagliaProdotto.decrementa_quantita(id_prodotto, id_taglia, quantita_da_decrementare)

            return redirect("utente/effettua_ordine")
        except mysql.connector.Error as err:
            return redirect("utente/effettua_ordine")
