import nltk
from flask import Blueprint, render_template, request, session, redirect, url_for

from models.Prodotto import search_products

app_bp = Blueprint('user_NLP', __name__)


@app_bp.route('/ricercaNLP', methods=['GET', 'POST'])
def search():
    # if 'logged_in' not in session or not session['logged_in']:
    #    return redirect(url_for('user_login.login_page'))

    try:
        if request.method == 'POST':

            query = request.form['text']

            # Utilizza il modello per cercare i prodotti nel database
            products = search_products(query)

            if products:
                return render_template('/utente/ricerca_NLP.html', data="test")
            else:
                return render_template('/utente/ricerca_NLP.html')
    except Exception as e:
        return render_template('/utente/ricerca_NLP.html', message='Errore con il server')

    return render_template('/utente/ricerca_NLP.html')
