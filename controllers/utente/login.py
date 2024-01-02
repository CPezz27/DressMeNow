import mysql.connector
from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Utente
from utils.utils import is_valid_password

app_bp = Blueprint('user_login', __name__)


@app_bp.route('/login')
def login_page():
    return render_template('utente/login.html')


@app_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not is_valid_password(password):
            return render_template('utente/login.html', message="La password non rispetta i criteri richiesti.")

        try:
            user = Utente.login(email, password)

            if user:
                session['logged_in'] = True
                session['id'] = user[0]
                return redirect('utente/profilo')
            else:
                return render_template('utente/login.html', message="Credenziali non valide. Riprova.")
        except mysql.connector.Error as err:
            return render_template('utente/login.html', message="Errore nel server. Riprova più tardi.")

    return redirect('utente/login')
