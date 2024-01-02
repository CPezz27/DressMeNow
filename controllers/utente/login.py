import mysql.connector
from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Utente
from utils import mysql_config
from utils.utils import is_valid_password

app_bp = Blueprint('user_login', __name__)

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


@app_bp.route('/login')
def login_page():
    return render_template('utente/login.html')


@app_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not is_valid_password(password):
            return render_template('login.html', message="La password non rispetta i criteri richiesti.")

        if conn:
            try:
                user = Utente.login(email, password)

                if user:
                    session['logged_in'] = True
                    session['email'] = email
                    return redirect(url_for('utente/profilo.html'))
                else:
                    return "Credenziali non valide. Riprova."
            except mysql.connector.Error as err:
                print(f"Errore durante l'esecuzione della query: {err}")
            finally:
                cursor.close()
                conn.close()

    return redirect('utente/login.html')
