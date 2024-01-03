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
        order_id = order[0]
        if order_id not in order_dict:
            order_dict[order_id] = {
                'order_details': {
                    'id_ordine': order_id,
                    'stato_ordine': order[1],
                    'data_ordine': order[2]
                },
                'transaction_details': {
                    'id_transazione': order[3],
                    'totale': order[5],
                    'stato_transazione': order[6]
                },
                'products': []
            }

        order_dict[order_id]['products'].append({
            'id_prodotto': order[7],
            'nome_prodotto': order[8],
            'prezzo_individuale': order[10],
        })

    user_orders = list(order_dict.values())

    print(user_orders)

    return render_template("utente/ordini.html", data=user_orders)
