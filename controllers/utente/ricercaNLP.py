import nltk
from flask import Blueprint, render_template, request, session, redirect

from models.Prodotto import search_products

app_bp = Blueprint('user_NLP', __name__)


@app_bp.route('/ricerca', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']

        # Utilizza il modello per cercare i prodotti nel database
        products = search_products(query)

        if products:
            return render_template('/utente/ricerca_NLP.html', data="test")
        else:
            return render_template('/utente/ricerca_NLP.html')

    return redirect('/')
