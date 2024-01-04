from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Utente
from models.Utente import Utente
from utils.utils import validate_input, is_valid_password
import mysql.connector


app_bp = Blueprint('modifica_profilo', __name__)


@app_bp.route('/profilo/modifica', methods=['GET', 'POST'])
def modifica_profilo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'GET':
        user_id = session.get('id')

        if user_id:
            user = Utente.get_user(id=user_id)

            if user:
                return render_template('modifica_profilo.html', user=user)  # Pagina per la modifica
            else:
                return render_template('profilo.html', message="Utente non trovato.")
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

            pattern_n = r'^[A-Za-z ]+$'
            pattern_data = r'^\d{4}-\d{2}-\d{2}$'
            pattern_telefono = r'^[0-9]+$'
            pattern_sesso = r'^(Uomo|Donna)$'
            pattern_email = r'^\S+@\S+\.\S+$'

            if not all([
                validate_input(nuovi_valori['nome'], pattern_n),
                validate_input(nuovi_valori['cognome'], pattern_n),
                validate_input(nuovi_valori['data_nascita'], pattern_data),
                validate_input(nuovi_valori['telefono'], pattern_telefono),
                validate_input(nuovi_valori['sesso'], pattern_sesso),
                validate_input(nuovi_valori['email'], pattern_email),
                is_valid_password(request.form['password'])
            ]):
                return render_template('profilo.html', message="Dati inseriti non validi. Controlla i campi e riprova.")

            try:
                utente = Utente.get_user(user_id)
                if utente:
                    utente_mod = {
                        'nome': nuovi_valori['nome'],
                        'cognome': nuovi_valori['cognome'],
                        'email': nuovi_valori['email'],
                        'password': request.form['password'],
                        'sesso': nuovi_valori['sesso'],
                        'numero_telefono': nuovi_valori['telefono'],
                        'data_nascita': nuovi_valori['data_nascita']
                    }
                    Utente.modifica_account(user_id, **utente_mod)
                    return redirect(url_for('user_profile.profilo'))
                else:
                    return render_template('404.html', message="Utente non trovato.")
            except mysql.connector.Error as err:
                return None
        else:
            return render_template('/login')
