from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Personale, Ordine, ProdottoInOrdine
from models.Personale import Personale

app_bp = Blueprint('user_controller', __name__)


@app_bp.route("/d/")
def visualizza_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    personale = Personale.get_all_personale()
    return render_template("direttore/personale.html", data=personale)


@app_bp.route("/d/aggiungi_personale", methods=['GET', 'POST'])
def aggiungi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

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
            return render_template("direttore/personale.html", message="Personale creato correttamente.")
        else:
            return render_template("direttore/personale.html", message="Personale non creato.")

    return render_template("direttore/aggiungi_personale.html")


@app_bp.route("/d/modifica_personale", methods=['GET', 'POST'])
def modifica_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tipo_personale = request.form['tipo_personale']
        flag = Personale.update_personale(email, password, tipo_personale)
        if flag:
            return render_template("direttore/modifica_personale.html", message="Personale modificato correttamente.")
        else:
            return render_template("direttore/modifica_personale.html", message="Personale non modificato.")

    return render_template("direttore/modifica_personale.html")


@app_bp.route("/d/rimuovi_personale", methods=['POST'])
def rimuovi_personale():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

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

    try:
        vendite_totali = Ordine.calcola_vendite_totali()

        guadagno = Ordine.calcola_guadagno()

        prodotti_resi = ProdottoInOrdine.conta_prodotti_resi()

        percentuale_resi = ProdottoInOrdine.percentuale_prodotti_resi()

        return render_template("utente/statistiche_ordini.html",
                               vendite_totali=vendite_totali,
                               guadagno=guadagno,
                               prodotti_resi=prodotti_resi,
                               percentuale_resi=percentuale_resi)
    except Exception as e:
        return render_template("errore.html", message="Errore durante il recupero delle statistiche ordini.")
