from flask import Blueprint, render_template, request, redirect, url_for, session

from models import Prodotto
from models.Prodotto import view_product
from models.Prodotto import update_prodotto
from models.Prodotto import delete

from models.Prodotto import Prodotto

app_bp = Blueprint('gestore_prodotti', __name__)


@app_bp.route('/aggiungi_prodotto')
def aggiunta():
    return render_template('aggiungiProdotto.html')


# Alfredo n si pone questa domanda: ma a che serve 'sta funzione?

@app_bp.route('/gp/prodotti', methods=['POST'])
def prodotti():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))

    return render_template('/gestore_prodotti/prodotti.html')


@app_bp.route('/gp/aggiungi_prodotto', methods=['POST'])
def aggiungi_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        marca = request.form['marca']
        descrizione = request.form['descrizione']
        vestibilita = request.form['vestibilita']
        prezzo = request.form['prezzo']
        colore = request.form['colore']
        materiale = request.form['materiale']
        #id_taglia = request.form['taglia']
        #quantita = request.form['quantita']

        try:
            nuovo_prodotto = Prodotto(
                nome=nome,
                categoria=categoria,
                marca=marca,
                descrizione=descrizione,
                vestibilita=vestibilita,
                prezzo=prezzo,
                colore=colore,
                materiale=materiale,
                #id_taglia=id_taglia,
                #quantita=quantita
            )

            #dopo aver inserito il prodotto mi prendo l'id generato 
            successo, id_prodotto = nuovo_prodotto.save()
            return redirect_to_aggiunta_taglia(id_prodotto)
        except Exception as err:
            return render_template('aggiungiProdotto.html', messaggio="Errore")


def redirect_to_aggiunta_taglia(id_prodotto):
    return redirect(url_for('taglia_controller.aggiunta_taglia', id_prodotto=id_prodotto))


@app_bp.route('/gp/modifica_prodotto/<int:product_id>', methods=['GET', 'POST'])
def modifica_prodotto(product_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))

    product = view_product(int(product_id))

    if request.method == 'POST':
        try:
            update_prodotto(product_id, **request.form)
            product = view_product(int(product_id))
            return render_template('modificaProdotto.html', product=product, message="Prodotto modificato correttamente")
        except Exception as err:
            return render_template('modificaProdotto.html', message="Errore durante la modifica")

    return render_template('modificaProdotto.html', product=product)

# in teoria si può eliminare secondo PL7 sium calabrese


@app_bp.route('/gp/elimina_prodotto/<int:product_id>', methods=['GET', 'POST'])
def elimina_prodotto(product_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))
    try:
        delete(int(product_id))
        return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto eliminato con successo"))
    except Exception as err:
        return render_template('modificaProdotto.html', message="Errore durante l'eliminazione")


@app_bp.route('/gp/mostra_prodotto', methods=['GET'])
def mostra_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))

    product_id=request.args.get('product_id')
    product = view_product(int(product_id))

    return render_template('modificaProdotto.html', product=product)


@app_bp.route('/gp/mostra_info_prodotti/', methods=['GET'])
def mostra_info_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index.homepage'))
    try:
        prodotti = mostra_info_prodotto()
    except Exception as err:
        return render_template('/gp/index.html', messaggio="Errore durante la visualizzazione")

    return render_template('/gp/prodotti.html', prodotti=prodotti)