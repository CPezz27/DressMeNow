from flask import Blueprint, request, render_template, session, redirect, url_for

from models import Carrello

app_bp = Blueprint('user_carrello', __name__)


@app_bp.route("/carrello")
def visualizza_carrello():
    try:
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('user_login.login_page'))

        user_id = session.get('id')

        prodotti = Carrello.contenuto_carrello(user_id)

        return render_template('/utente/carrello.html', data=prodotti)

    except Exception as e:
        return render_template('/utente/carrello.html', message='Errore con il server')


@app_bp.route("/aggiungi_al_carrello", methods=['POST'])
def aggiungi_al_carrello():
    if request.method == 'POST':
        try:
            if 'logged_in' not in session or not session['logged_in']:
                return redirect(url_for('user_login.login_page'))

            user_id = session.get('id')

            id_prodotto = request.form.get('id_prodotto')

            flag = Carrello.aggiungi_al_carrello(user_id, id_prodotto, 1)

            if flag:
                return render_template('/utente/carrello.html', message='Reso effettuato con successo')
            else:
                return render_template('/utente/carrello.html', message='Reso effettuato con successo')

        except Exception as e:
            return render_template('/utente/carrello.html', message='Errore con il server')


@app_bp.route("/rimuovi_dal_carrello", methods=['POST'])
def rimuovi_dal_carrello():
    if request.method == 'POST':
        try:
            if 'logged_in' not in session or not session['logged_in']:
                return redirect(url_for('user_login.login_page'))

            user_id = session.get('id')

            id_prodotto = request.form.get('id_prodotto')

            flag = Carrello.rimuovi_dal_carrello(user_id, id_prodotto)

            if flag:
                return render_template('/utente/carrello.html', message='Prodotto rimosso con successo')
            else:
                return render_template('/utente/carrello.html', message='Prodotto non rimosso')

        except Exception as e:
            return render_template('/utente/carrello.html', message='Errore con il server')


@app_bp.route("/svuota_carrello", methods=['POST'])
def svuota_carrello():
    if request.method == 'POST':
        try:
            if 'logged_in' not in session or not session['logged_in']:
                return redirect(url_for('user_login.login_page'))

            user_id = session.get('id')

            flag = Carrello.svuota_carrello(user_id)

            if flag:
                return render_template('/utente/carrello.html', message='Carrello svuotato con successo')
            else:
                return render_template('/utente/carrello.html', message='Carrello non svuotato')

        except Exception as e:
            return render_template('/utente/carrello.html', message='Errore con il server')
