from flask import Blueprint, request, render_template, session, redirect, url_for

from models import Carrello

app_bp = Blueprint('user_carrello', __name__)


@app_bp.route("/carrello")
def visualizza_carrello():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    try:
        user_id = session.get('id')

        prodotti, totale = Carrello.contenuto_carrello(user_id)

        return render_template('/utente/carrello.html', data=prodotti, totale=totale)

    except Exception as e:
        return render_template('/utente/carrello.html', message='Errore con il server')


@app_bp.route("/aggiungi_al_carrello", methods=['POST'])
def aggiungi_al_carrello():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        try:
            user_id = session.get('id')

            id_prodotto = request.form.get('id_prodotto')
            size = request.form.get('size')
            quantity = request.form.get('quantity')

            flag = Carrello.aggiungi_al_carrello(user_id, id_prodotto, size, quantity)

            if flag:
                message = 'Prodotto aggiunto al carrello correttamente'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))
            else:
                message = 'Problema 1'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))

        except Exception as e:
            message = 'Problema 2'
            return redirect(url_for('user_carrello.visualizza_carrello', message=message))


@app_bp.route("/rimuovi_dal_carrello", methods=['POST'])
def rimuovi_dal_carrello():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        try:
            user_id = session.get('id')

            id_prodotto = request.form.get('id_prodotto')

            flag = Carrello.rimuovi_dal_carrello(user_id, id_prodotto)

            if flag:
                message = 'Prodotto rimosso con successo'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))
            else:
                message = 'Prodotto non rimosso'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))

        except Exception as e:
            message = 'Errore con il server'
            return redirect(url_for('user_carrello.visualizza_carrello', message=message))


@app_bp.route("/svuota_carrello", methods=['POST'])
def svuota_carrello():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        try:
            user_id = session.get('id')

            flag = Carrello.svuota_carrello(user_id)

            if flag:
                message = 'Carrello svuotato con successo'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))
            else:
                message = 'Carrello non svuotato'
                return redirect(url_for('user_carrello.visualizza_carrello', message=message))

        except Exception as e:
            message = 'Errore con il server'
            return redirect(url_for('user_carrello.visualizza_carrello', message=message))
