from flask import Blueprint, render_template, request, redirect, url_for
from models import Prodotto
from models.Prodotto import Prodotto

prodotto_bp = Blueprint('gestore_prodotti', __name__)


@prodotto_bp.route('/gestore_prodotti/prodotti')
def prodotti():
    return render_template('/gestore_prodotti/prodotti.html')


@prodotto_bp.route('/gestore_prodotti/aggiungi_prodotto', methods=['POST'])
def aggiungi_prodotto():
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
            return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto aggiunto con successo"))
        except Exception as err:
            return render_template('/gestore_prodotti/aggiungi_prodotto.html', messaggio="Errore durante l'aggiunta del prodotto")

    return render_template('/gestore_prodotti/aggiungi_prodotto.html') 


@prodotto_bp.route('/gestore_prodotti/modifica_prodotto/<int:product_id>', methods=['GET', 'POST'])
def modifica_prodotto(product_id):
    
    prodotto_da_modificare = Prodotto.view_product(product_id)

    if request.method == 'POST':
        try:
            Prodotto.update_prodotto(product_id, **request.form)
            return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto modificato con successo"))
        except Exception as err:
            return render_template('/gestore_prodotti/modifica_prodotto.html', messaggio="Errore durante la modifica del prodotto")

    return render_template('/gestore_prodotti/modifica_prodotto.html', prodotto=prodotto_da_modificare)


@prodotto_bp.route('/gestore_prodotti/elimina_prodotto/<int:product_id>', methods=['POST'])
def elimina_prodotto(product_id):
    try:
        Prodotto.delete(product_id)
        return redirect(url_for('gestione_prodotto.prodotti', message="Prodotto eliminato con successo"))
    except Exception as err:
        return render_template('/gestore_prodotti/modifica_prodotto.html', messaggio= "Errore durante l'eliminazione del prodotto")
