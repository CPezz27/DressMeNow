from flask import Blueprint, render_template, request, redirect, session, url_for

from models import Immagine
from models.Immagine import Immagine
from models.Immagine import visualizza_immagini_prodotto
from base64 import b64encode

app_bp = Blueprint('image_controller', __name__)


@app_bp.route("/gp/aggiungi_immagine", methods=['GET', 'POST'])
def aggiungi_immagine():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_prodotto = int(request.form['id_prodotto'])
        tipo = request.form['tipo_immagine']
        image_file = request.files['immagine']

        immagine = Immagine(id_prodotto, image_file, tipo)

        success = immagine.save()

        if success:
            immagini = visualizza_immagini_prodotto(id_prodotto)

            return render_template("aggiungiImgProdotto.html", data=immagini, message="Immagine inserita correttamente")
        else:
            immagini = visualizza_immagini_prodotto(id_prodotto)

            return render_template("aggiungiImgProdotto.html", data=immagini, message="Errore nell'inserimento dell'immagine")

    return render_template("gestore_prodotti/aggiungi_immagine.html")


@app_bp.route("/gp/rimuovi_immagine/<int:id_immagine>", methods=['POST'])
def rimuovi_immagine(id_immagine):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    success = Immagine.rimuovi_immagine(id_immagine)

    if success:
        return render_template("gestore_prodotti/immagini.html")  # mess. successo
    else:
        return render_template("gestore_prodotti/immagini.html")  # mess. errore


@app_bp.route("/gp/visualizza_immagini", methods=['POST'])
def visualizza_immagini():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    immagini = Immagine.visualizza_immagini()

    return render_template("gestore_prodotti/immagini.html", data=immagini)


@app_bp.route("/gp/visualizza_immagini_prodotto/<int:id_prodotto>", methods=['GET', 'POST'])
def visualizza_immagini_prodott(id_prodotto):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    print("\n\nSonoQUI\n\n")
    immagini = visualizza_immagini_prodotto(id_prodotto)

    return render_template("aggiungiImgProdotto.html", data=immagini)