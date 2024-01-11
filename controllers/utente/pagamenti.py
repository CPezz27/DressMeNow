import decimal
from datetime import date

from flask import Blueprint, request, redirect, url_for
import requests

from models.Ordine import Ordine
from models.ProdottoInOrdine import ProdottoInOrdine
from models.Transazione import Transazione

app_bp = Blueprint('user_payments', __name__)


@app_bp.route('/verifica_pagamento', methods=['GET', 'POST'])
def verifica_pagamento():
    transaction_details = request.get_json()

    order_id = transaction_details['id']

    paypal_api_url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PAYPAL_ACCESS_TOKEN'
    }

    try:
        response = requests.get(paypal_api_url, headers=headers)
        if response.status_code == 200:
            paypal_order_details = response.json()

            id_utente = paypal_order_details['custom']['id_utente']
            data_transazione = date.today()
            totale_transazione = decimal.Decimal(paypal_order_details['purchase_units'][0]['amount']['value'])
            stato_transazione = 'Confermato'

            ordine = Ordine(id_utente=id_utente, stato=stato_transazione, data=data_transazione)
            id_ordine = ordine.save()

            transazione = Transazione(id_utente=id_utente, id_ordine=id_ordine, data=data_transazione, totale=totale_transazione, stato=stato_transazione)
            transazione.save()

            for item in paypal_order_details['purchase_units'][0]['items']:
                id_prodotto = item['custom']['id_prodotto']

                prodotto_in_ordine = ProdottoInOrdine(id_ordine=id_ordine, id_prodotto=id_prodotto, reso=0,
                                                      stato_reso=None, note_reso=None)
                prodotto_in_ordine.save()

            return redirect(url_for('conferma_ordine'))
        else:
            return redirect(url_for('errore_ordine'))
    except requests.RequestException as e:
        return redirect(url_for('errore_ordine'))
