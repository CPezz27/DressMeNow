from flask import Blueprint, render_template, session, redirect

from models import Utente

app_bp = Blueprint('user_profile', __name__)


@app_bp.route("/utente/profilo")
def profilo():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    user = Utente.get_user(user_id)

    return render_template("utente/profilo.html", data=user)


@app_bp.route("/utente/indirizzi")
def indirizzi():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    addresses = Utente.get_addresses(user_id)

    print(addresses)

    return render_template("utente/indirizzi.html", data=addresses)


@app_bp.route("/utente/ordini")
def orders():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    orders = Utente.get_addresses(user_id)

    return render_template("utente/ordini.html", data=orders)

