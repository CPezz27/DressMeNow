import decimal
from datetime import date

from flask import Blueprint, request, redirect, url_for, session, render_template
import requests

from models import Carrello
from models.Ordine import Ordine
from models.ProdottoInOrdine import ProdottoInOrdine
from models.Transazione import Transazione

app_bp = Blueprint('user_payments', __name__)


@app_bp.route('/conferma_ordine', methods=['GET'])
def conferma_ordine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    try:
        return render_template('/confermaOrdine.html')
    except Exception as e:
        return render_template('/confermaOrdine.html')


@app_bp.route('/pagamento', methods=['GET'])
def pagamento():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    try:
        user_id = session.get('id')

        prodotti, totale = Carrello.contenuto_carrello(user_id)

        return render_template('/utente/pagamento.html', data=prodotti, totale=totale)

    except Exception as e:
        return render_template('/utente/pagamento.html', message='Errore con il server')


@app_bp.route('/verifica_pagamento', methods=['GET', 'POST'])
def verifica_pagamento():
    total_price = request.form.get('price')
    items = request.form.get('items')
    try:
        id_utente = session['id']
        data_transazione = date.today()
        totale_transazione = total_price
        stato_transazione = 'Confermato'

        ordine = Ordine(id_utente=id_utente, stato=stato_transazione, data=data_transazione)
        id_ordine = ordine.save()

        transazione = Transazione(id_utente=id_utente, id_ordine=id_ordine, data=data_transazione,
                                  totale=totale_transazione, stato=stato_transazione)
        transazione.save()

        for item in items:
            id_prodotto = item

            prodotto_in_ordine = ProdottoInOrdine(id_ordine=id_ordine, id_prodotto=id_prodotto, reso=0,
                                                  stato_reso=None, note_reso=None)
            prodotto_in_ordine.save()

            Carrello.rimuovi_dal_carrello(id_utente, id_prodotto)

        return redirect(url_for('user_payments.conferma_ordine'))
    except requests.RequestException as e:
        return redirect(url_for('user_login.login_page'))
