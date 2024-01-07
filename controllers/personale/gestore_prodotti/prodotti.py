from flask import Blueprint, render_template, request, redirect, url_for, session

from models import Prodotto
from models.Prodotto import Prodotto

app_bp = Blueprint('gestore_prodotti', __name__)


@app_bp.route('/aggiungi_prodotto')
def aggiunta():
    return render_template('aggiungiProdotto.html')


@app_bp.route('/gp/prodotti')
def prodotti():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    return render_template('/gestore_prodotti/prodotti.html')


@app_bp.route('/gp/aggiungi_prodotto', methods=['POST'])
def aggiungi_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        marca = request.form['marca']
        descrizione = request.form['descrizione']
        vestibilita = request.form['vestibilita']
        prezzo = request.form['prezzo']
        colore = request.form['colore']
        materiale = request.form['materiale']

        try:
            nuovo_prodotto = Prodotto(
                nome=nome,
                categoria=categoria,
                marca=marca,
                descrizione=descrizione,
                vestibilita=vestibilita,
                prezzo=prezzo,
                colore=colore,
                materiale=materiale
            )
            nuovo_prodotto.save()
            return redirect(url_for('gestione_prodotto.aggiungiProdotto', message="Prodotto aggiunto con successo"))
        except Exception as err:
            return render_template('aggiungiProdotto.html', messaggio="Errore")

    return render_template('aggiungiProdotto.html')


@app_bp.route('/gp/modifica_prodotto/<int:product_id>', methods=['GET', 'POST'])
def modifica_prodotto(product_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    prodotto_da_modificare = Prodotto.view_product(product_id)

    if request.method == 'POST':
        try:
            Prodotto.update_prodotto(product_id, **request.form)
            return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto modificato con successo"))
        except Exception as err:
            return render_template('/gestore_prodotti/modifica_prodotto.html', messaggio="Errore durante la modifica")

    return render_template('/gestore_prodotti/modifica_prodotto.html', prodotto=prodotto_da_modificare)


@app_bp.route('/gp/elimina_prodotto/<int:product_id>', methods=['POST'])
def elimina_prodotto(product_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    try:
        Prodotto.delete(product_id)
        return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto eliminato con successo"))
    except Exception as err:
        return render_template('/gestore_prodotti/modifica_prodotto.html', messaggio="Errore durante l'eliminazione")
    

@app_bp.route('/gp/mostra_info_prodotti/', methods=['GET'])
def mostra_info_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))
    try:
        prodotti = mostra_info_prodotto()
    except Exception as err:
        return render_template('/gp/index.html', messaggio="Errore durante la visualizzazione")

    return render_template('/gp/prodotti.html', prodotti=prodotti)