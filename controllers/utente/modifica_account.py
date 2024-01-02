from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Utente
import mysql.connector
from utils.utils import validate_input
from utils.utils import is_valid_password

#Modifiche da effettuare

app_bp = Blueprint('modifica_profilo', __name__)


@app_bp.route('/profilo/modifica', methods=['GET', 'POST'])
def modifica_profilo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'GET':
        user_id = session.get('id')

        if user_id:
            user = Utente.get_user(user_id)

            if user:
                return render_template('modifica_profilo.html', user=user) #pagina per la modifica
            else:
                return render_template('404.html', message="Utente non trovato.")
        else:
            return render_template('/login')

    elif request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            nuovi_valori = {
                'nome': request.form['nome'],
                'cognome': request.form['cognome'],
                'email': request.form['email'],
                'data_nascita': request.form['data_nascita'],
                'telefono': request.form['telefono'],
                'sesso': request.form['sesso']
            }



            if not all([
                validate_input(nome, pattern_n),
                validate_input(cognome, pattern_n),
                validate_input(data_nascita, pattern_data),
                validate_input(telefono, pattern_telefono),
                validate_input(sesso, pattern_sesso),
                validate_input(email, pattern_email),
                validate_input(password, pattern_password)
            ]):
                return "Dati inseriti non validi. Controlla i campi e riprova."

            try:
                utente = Utente() #stesso problema di effettua ordine
                utente.modifica_account(user_id, nuovi_valori)
                return redirect(url_for('user_profile.profilo'))
            except mysql.connector.Error as err:
                print(f"Errore durante la modifica dell'account: {err}")
                return render_template('profilo.html', message="Errore durante la modifica dell'account.")
        else:
            return render_template('/login')
