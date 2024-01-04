from flask import Blueprint, render_template, session, redirect, url_for, request

from models import Utente, ConfigurazioneAvatar
from models import Ordine

import mysql.connector

from utils.utils import validate_input, is_valid_password

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

    return render_template("utente/ordini.html", data=user_orders)


@app_bp.route('/p/cancella_account', methods=['POST'])
def delete_account():

    if 'id' not in session:
        return redirect('utente/login')

    try:
        user_id = session['id']
        Utente.delete_account(user_id)

        session.pop('id', None)
        session.pop('logged_in', None)

        return redirect(url_for('homepage'))

    except mysql.connector.Error as err:
        print(f"Errore durante la cancellazione dell'account: {err}")
        return redirect(url_for('profilo', message='Si è verificato un errore'))


@app_bp.route('/p/modifica_account', methods=['GET', 'POST'])
def modifica_profilo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'GET':
        user_id = session.get('id')

        if user_id:
            user = Utente.get_user(id=user_id)

            if user:
                return render_template('modifica_profilo.html', user=user)  # Pagina per la modifica
            else:
                return render_template('profilo.html', message="Utente non trovato.")
        else:
            return render_template('/login')

    elif request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            nuovi_valori = {
                'nome': request.form['nome'],
                'cognome': request.form['cognome'],
                'email': request.form['email'],
                'data_nascita': request.form['data_nascita'],
                'telefono': request.form['telefono'],
                'sesso': request.form['sesso']
            }

            pattern_n = r'^[A-Za-z ]+$'
            pattern_data = r'^\d{4}-\d{2}-\d{2}$'
            pattern_telefono = r'^[0-9]+$'
            pattern_sesso = r'^(Uomo|Donna)$'
            pattern_email = r'^\S+@\S+\.\S+$'

            if not all([
                validate_input(nuovi_valori['nome'], pattern_n),
                validate_input(nuovi_valori['cognome'], pattern_n),
                validate_input(nuovi_valori['data_nascita'], pattern_data),
                validate_input(nuovi_valori['telefono'], pattern_telefono),
                validate_input(nuovi_valori['sesso'], pattern_sesso),
                validate_input(nuovi_valori['email'], pattern_email),
                is_valid_password(request.form['password'])
            ]):
                return render_template('profilo.html', message="Dati inseriti non validi. Controlla i campi e riprova.")

            try:
                utente = Utente.get_user(user_id)
                if utente:
                    utente_mod = {
                        'nome': nuovi_valori['nome'],
                        'cognome': nuovi_valori['cognome'],
                        'email': nuovi_valori['email'],
                        'password': request.form['password'],
                        'sesso': nuovi_valori['sesso'],
                        'numero_telefono': nuovi_valori['telefono'],
                        'data_nascita': nuovi_valori['data_nascita']
                    }
                    Utente.modifica_account(user_id, **utente_mod)
                    return redirect(url_for('user_profile.profilo'))
                else:
                    return render_template('404.html', message="Utente non trovato.")
            except mysql.connector.Error as err:
                return None
        else:
            return render_template('/login')


@app_bp.route("/p/configura_avatar", methods=['POST'])
def configura_avatar():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('utente/login')

    user_id = session['id']

    if request.method == 'POST':
        data = request.json
        if data:
            success = ConfigurazioneAvatar.update_configurazione_avatar(user_id, **data)
            if success:
                return render_template("utente/avatar.html", message="Avatar aggiornato correttamente.")
            else:
                return render_template("utente/avatar.html", message="Avatar non aggiornato.")
        else:
            return render_template("utente/avatar.html", message="Parametri mancanti.")
