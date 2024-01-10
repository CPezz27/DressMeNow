from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Personale, Ordine, ProdottoInOrdine, Utente
from models.Personale import Personale, get_all_personale, update_personale, view_personale
from models.Utente import Utente, get_all_users, modifica_account

app_bp = Blueprint('direttore_controller', __name__)


@app_bp.route("/d/visualizza_utenti")
def visualizza_utenti():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index'))

    utente = get_all_users()
    return render_template("direttore/gestione_utenti.html", data=utente)


@app_bp.route("/d/dashboard")
def visualizza_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index'))

    personale = get_all_personale()
    print(personale)
    return render_template("direttore/index.html", data=personale)


@app_bp.route("/d/aggiungi_personale", methods=['GET', 'POST'])
def aggiungi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index'))

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
        return redirect(url_for('index'))

    personale = view_personale(int(id_personale))
    print(personale)

    if request.method == 'POST':
        try:
            updated_data = {
                'id_personale': request.form['password'],
                'email': request.form['email'],
                'password': request.form['password'],
                'tipo_personale': request.form['tipo_personale']
            }

            update_personale(id_personale, **updated_data)

            personale = view_personale(int(id_personale))
            return render_template('direttore/modifica_personale.html', personale=personale, message="Prodotto modificato")

        except Exception as err:
            return render_template('direttore/modifica_personale.html', message="Errore durante la modifica")

    return render_template('direttore/modifica_personale.html', personale=personale)


@app_bp.route("/d/rimuovi_personale", methods=['POST'])
def rimuovi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'direttore':
        return redirect(url_for('index'))

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
        return redirect(url_for('index'))

    try:
        vendite_totali = Ordine.calcola_vendite_totali()
        print("vendite totali", vendite_totali)
        guadagno = Ordine.calcola_guadagno()
        print("calcolo guadagno:", guadagno)
        prodotti_resi = ProdottoInOrdine.conta_prodotti_resi()
        print("conta prodotti resi:", prodotti_resi)
        percentuale_resi = ProdottoInOrdine.percentuale_prodotti_resi()
        print("perc prodotti resi:", percentuale_resi)
        return render_template("/direttore/statistiche.html",
                               vendite_totali=vendite_totali,
                               guadagno=guadagno,
                               prodotti_resi=prodotti_resi,
                               percentuale_resi=percentuale_resi)
    except Exception as e:
        return render_template("500.html", message="Errore durante il recupero delle statistiche ordini.")
