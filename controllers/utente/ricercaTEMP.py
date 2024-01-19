from flask import Blueprint, render_template, request, session, redirect, url_for

app_bp = Blueprint('user_NLP', __name__)


@app_bp.route('/ricercaNLP', methods=['GET', 'POST'])
def search():
    return render_template('/utente/ricerca_NLP.html')


@app_bp.route('/risultatiNLP', methods=['GET', 'POST'])
def search2():
    return render_template('/utente/risultati_NLP.html')
