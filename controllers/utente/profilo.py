import mysql.connector
from flask import Blueprint, render_template, session, redirect, url_for, request

from models import Ordine
from models import Utente, ConfigurazioneAvatar
from models.Indirizzo import get_addresses
from utils.utils import validate_input, is_valid_password

app_bp = Blueprint('user_profile', __name__)


@app_bp.route("/p/impostazioni")
def impostazioni():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session['id']

    user = Utente.get_user(user_id)

    return render_template("utente/impostazioni.html", data=user)


@app_bp.route("/p/profilo")
def profilo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session['id']

    user = Utente.get_user(user_id)

    return render_template("utente/profilo.html", data=user)


@app_bp.route("/p/indirizzi")
def indirizzi():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    print("Sono prima nell'altro modulo")
    user_id = session['id']
    print("Sono nell'altro modulo", user_id)

    addresses = get_addresses(int(user_id))

    print(addresses)

    return render_template("utente/indirizzi.html", data=addresses)


@app_bp.route("/p/ordini")
def orders():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

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
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    try:
        user_id = session.get('id')
        Utente.delete_account(user_id)

        session.pop('id', None)
        session.pop('logged_in', None)

        return redirect(url_for('user_login.login_page'))

    except mysql.connector.Error as err:
        print(f"Errore durante la cancellazione dell'account: {err}")
        return redirect(url_for('profilo', message='Si è verificato un errore'))


@app_bp.route('/p/modifica_account', methods=['GET', 'POST'])
def modifica_profilo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            nuovi_valori = {
                'nome': request.form.get('nome'),
                'cognome': request.form.get('cognome'),
                'data_nascita': request.form.get('data_nascita'),
                'telefono': request.form.get('telefono'),
                'sesso': request.form.get('sesso')
            }

            try:
                utente = Utente.get_user(user_id)
                if utente:
                    utente_mod = {
                        'nome': nuovi_valori['nome'],
                        'cognome': nuovi_valori['cognome'],
                        'sesso': nuovi_valori['sesso'],
                        'telefono': nuovi_valori['telefono'],
                        'data_nascita': nuovi_valori['data_nascita']
                    }
                    Utente.modifica_account(user_id, **utente_mod)
                    return redirect(url_for('user_profile.profilo'))
                else:
                    return render_template('404.html', message="Utente non trovato.")
            except mysql.connector.Error as err:
                return redirect(url_for('user_login.login_page'))
        else:
            return redirect(url_for('user_login.login_page'))


@app_bp.route("/p/configura_avatar", methods=['GET', 'POST'])
def configura_avatar():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('utente/login')

    user_id = session['id']

    avatar = ConfigurazioneAvatar.view_avatar(user_id)

    if request.method == 'POST':
        data = request.json
        if data:
            success = ConfigurazioneAvatar.update_configurazione_avatar(
                user_id, **data)
            if success:
                return render_template("utente/personalizzazioneAvatar.html", data=avatar, message="Avatar aggiornato correttamente.")
            else:
                return render_template("utente/personalizzazioneAvatar.html", data=avatar, message="Avatar non aggiornato.")
        else:
            return render_template("utente/personalizzazioneAvatar.html", data=avatar, message="Parametri mancanti.")

    return render_template("utente/personalizzazioneAvatar.html", data=avatar)


@app_bp.route('/logout')
def logout():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    session.pop('id', None)
    session.pop('logged_in', None)
    return redirect(url_for('user_login.login_page'))
