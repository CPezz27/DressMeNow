from flask import Blueprint, render_template, session, redirect

from models import Utente
from models import Ordine

app_bp = Blueprint('user_profile', __name__)


@app_bp.route("/p/profilo")
def profilo():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    user = Utente.get_user(user_id)

    return render_template("utente/profilo.html", data=user)


@app_bp.route("/p/indirizzi")
def indirizzi():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    addresses = Utente.get_addresses(user_id)

    print(addresses)

    return render_template("utente/indirizzi.html", data=addresses)


@app_bp.route("/p/ordini")
def orders():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    user_orders = Ordine.get_user_orders(user_id)

    order_dict = {}
    for order in user_orders:
        order_id = order['id_ordine']
        if order_id not in order_dict:
            order_dict[order_id] = {
                'order_details': {
                    'id_ordine': order_id,
                    'stato_ordine': order['stato_ordine'],
                    'data_ordine': order['data_ordine']
                },
                'transaction_details': {
                    'id_transazione': order['id_transazione'],
                    'data_transazione': order['data_transazione'],
                    'totale': order['totale'],
                    'stato_transazione': order['stato_transazione']
                },
                'products': []
            }

        order_dict[order_id]['products'].append({
            'id_prodotto': order['id_prodotto'],
            'nome_prodotto': order['nome_prodotto'],
            'reso': order['reso'],
            'stato_reso': order['stato_reso'],
            'note_reso': order['note_reso']
        })

    user_orders = list(order_dict.values())

    return render_template("utente/ordini.html", data=user_orders)


