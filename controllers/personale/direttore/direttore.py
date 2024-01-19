from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Personale, Ordine, ProdottoInOrdine, Utente
from models.Personale import Personale, get_all_personale, update_personale, view_personale
from models.Utente import Utente, get_all_users, modifica_account, view_utente, update_utente

app_bp = Blueprint('direttore_controller', __name__)


@app_bp.route("/d/visualizza_utenti")
def visualizza_utenti():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    utente = get_all_users()
    return render_template("direttore/gestione_utenti.html", data=utente)


@app_bp.route("/d/dashboard")
def visualizza_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    personale = get_all_personale()

    return render_template("direttore/index.html", data=personale)


@app_bp.route("/d/aggiungi_personale", methods=['GET', 'POST'])
def aggiungi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tipo_personale = request.form['tipo_personale']
        personale = Personale(
            email=email,
            password=password,
            tipo_personale=tipo_personale
        )
        flag = personale.save()
        if flag:
            return render_template("direttore/aggiunta_personale.html", message="Personale creato correttamente.")
        else:
            return render_template("direttore/aggiunta_personale.html", message="Personale non creato.")

    return render_template("direttore/aggiunta_personale.html")


@app_bp.route("/d/modifica_personale/<int:id_personale>", methods=['GET', 'POST'])
def modifica_personale(id_personale):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session.get('ruolo') != 'direttore':
        return redirect(url_for('index.homepage'))

    if request.method == 'POST':
        try:
            update_personale(id_personale, **request.form)

            return redirect(url_for('direttore_controller.mostra_personale', personal_id=id_personale, message="Personale modificato"))

        except Exception as err:
            return redirect(url_for('direttore_controller.mostra_personale', personal_id=id_personale, message="Errore durante la modifica"))


@app_bp.route('/d/mostra_personale', methods=['GET'])
def mostra_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    message = request.args.get('message', '')

    id_personale = request.args.get('personal_id')

    personale = view_personale(int(id_personale))


    return render_template('direttore/modifica_personale.html', personale=personale, message=message)


@app_bp.route('/d/mostra_utente', methods=['GET'])
def mostra_utente():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    id_utente = request.args.get('id_user')

    message = request.args.get('message', '')

    utente = view_utente(int(id_utente))


    return render_template('direttore/modifica_utente.html', utente=utente, message=message)


@app_bp.route('/d/modifica_utente', methods=['GET', 'POST'])
def modifica_utente():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session.get('ruolo') != 'direttore':
        return redirect(url_for('index.homepage'))

    id_utente = request.args.get('id_user')

    utente = view_utente(int(id_utente))

    if request.method == 'POST':
        try:
            update_utente(id_utente, **request.form)

            return redirect(url_for('direttore_controller.mostra_utente', id_user=id_utente,
                                    message="Utente modificato"))

        except Exception as err:
            return redirect(url_for('direttore_controller.mostra_utente', id_user=id_utente,
                                    message="Errore durante la modifica"))


@app_bp.route("/d/rimuovi_personale", methods=['POST'])
def rimuovi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    if request.method == 'POST':
        id_personale = request.form['id_personale']
        flag = Personale.delete_personale(id_personale)
        if flag:
            return render_template("direttore/personale.html", message="Personale rimosso correttamente.")
        else:
            return render_template("direttore/personale.html", message="Personale non rimosso.")


@app_bp.route("/d/statistiche_ordini")
def visualizza_statistiche_ordini():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index.homepage'))

    try:
        vendite_totali = Ordine.calcola_vendite_totali()
        guadagno = Ordine.calcola_guadagno()
        prodotti_resi = Ordine.conta_ordini_resi()
        percentuale_resi = Ordine.percentuale_ordini_resi()
        return render_template("/direttore/statistiche.html",
                               vendite_totali=vendite_totali,
                               guadagno=guadagno,
                               ordini_resi=prodotti_resi,
                               percentuale_resi=percentuale_resi)
    except Exception as e:
        return render_template("500.html", message="Errore durante il recupero delle statistiche ordini.")
