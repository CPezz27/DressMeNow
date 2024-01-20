from flask import Blueprint, render_template, request

from models.Prodotto import search_products

app_bp = Blueprint('user_NLP', __name__)


@app_bp.route('/ricercaNLP', methods=['GET', 'POST'])
def search():
    try:
        if request.method == 'POST':

            query = request.form['text']

            products = search_products(query)

            if products:
                return render_template('/utente/risultati_NLP.html', data=products)
            else:
                return render_template('/utente/risultati_NLP.html', data=None)
    except Exception as e:
        return render_template('/utente/ricerca_NLP.html', message='Errore con il server')

    return render_template('/utente/ricerca_NLP.html')
