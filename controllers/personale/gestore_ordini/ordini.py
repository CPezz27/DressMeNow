from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Ordine
from models.Ordine import visualizza_ordine

app_bp = Blueprint('order_controller', __name__)


@app_bp.route("/go/cancella_ordine", methods=['POST'])
def cancella_ordine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] is not 'gestore_ordine':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        success = cancella_ordine(id_ordine)

        if success:
            return render_template("success.html", message="Ordine cancellato correttamente.")
        else:
            return render_template("error.html", message="Errore durante la cancellazione dell'ordine.")


@app_bp.route("/go/modifica_stato_ordine", methods=['POST'])
def modifica_stato_ordine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] is not 'gestore_ordine':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        nuovo_stato = request.form['nuovo_stato']
        success = modifica_stato_ordine(id_ordine, nuovo_stato)

        if success:
            return render_template("success.html", message="Stato dell'ordine modificato correttamente.")
        else:
            return render_template("error.html", message="Errore durante la modifica dello stato dell'ordine.")


@app_bp.route("/go/modifica_ordine", methods=['POST'])
def modifica_ordine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] is not 'gestore_ordine':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        nuovo_stato = request.form['nuovo_stato']

        success = Ordine.modifica_ordine(id_ordine, nuovo_stato)

        if success:
            return render_template("successo.html", message="Stato dell'ordine modificato con successo.")
        else:
            return render_template("errore.html", message="Si è verificato un errore durante la modifica dell'ordine.")


@app_bp.route("/go/visualizza_ordine", methods=['GET'])
def visual_ordine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] is not 'gestore_ordine':
        return redirect(url_for('index'))

    try:
        id_ordine = request.args.get('id_ordine')

        if id_ordine is not None:
            order_details = visualizza_ordine(int(id_ordine))

            if order_details:
                return render_template("/gestore_ordini/visualizza_ordine.html", order_details=order_details)
            else:
                return render_template("/gestore_ordini/visualizza_ordine.html",
                                       message="Errore durante il recupero dei dettagli dell'ordine.")
        else:
            return render_template("/gestore_ordini/visualizza_ordine.html",
                                   message="Errore durante il recupero dei dettagli dell'ordine.")
    except Exception as e:
        return render_template("/gestore_ordini/visualizza_ordine.html",
                               message="Errore durante il recupero dei dettagli dell'ordine.")


@app_bp.route('/go/dashboard')
def dashboard():
    orders_details = Ordine.get_all_orders_with_details()
    
    return render_template('gestoreOrdine.html', orders_details=orders_details)
