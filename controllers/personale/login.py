import mysql.connector
from flask import Blueprint, render_template, request, redirect, session, url_for

from models import Personale
from utils import mysql_config

app_bp = Blueprint('direttore_login', __name__)

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


@app_bp.route('/direttore/login')
def login_page():
    return render_template('direttore/login.html')


@app_bp.route('/direttore/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if conn:
            try:
                direttore = Personale.login(email, password)

                if direttore:
                    session['logged_in'] = True
                    session['email'] = email

                    tipo_personale = direttore[3]

                    if tipo_personale == 'direttore':
                        session['ruolo'] = 'direttore'
                        return redirect(url_for('direttore_login.direttore'))
                    elif tipo_personale == 'gestore_ordine':
                        session['ruolo'] = 'gestore_ordine'
                        return redirect(url_for('direttore_login.gestore_ordine'))
                    elif tipo_personale == 'gestore_prodotto':
                        session['ruolo'] = 'gestore_prodotto'
                        return redirect(url_for('direttore_login.gestore_prodotto'))
                else:
                    return "Credenziali non valide. Riprova."
            except mysql.connector.Error as err:
                print(f"Errore durante l'esecuzione della query")
            finally:
                cursor.close()
                conn.close()


@app_bp.route('/gestore_ordine')
def gestore_ordine():
    return render_template('gestoreOrdine.html')


@app_bp.route('/gestore_prodotto')
def gestore_prodotto():
    return render_template('gestoreProdotto.html')


@app_bp.route('/direttore/')
def direttore():
    return render_template('direttore/index.html')
