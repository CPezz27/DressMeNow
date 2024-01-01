import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for

from models.Utente import Utente
from utils import mysql_config
from utils.utils import validate_input

app_bp = Blueprint('user_register', __name__)

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


@app_bp.route('/registrati')
def register_page():
    return render_template('registrazione.html')


@app_bp.route('/registrati', methods=['POST'])
def register():
    if request.method == 'POST':
        nome = request.form['firstName']
        cognome = request.form['lastName']
        data_nascita = request.form['dataNascita']
        telefono = request.form['NumeroTelefonico']
        sesso = request.form['sesso']
        email = request.form['email']
        password = request.form['confirmPassword']

        # Definizione delle regex
        pattern_n = r'^[a-zA-Z\s]{1,50}$'
        pattern_data = r'^\d{4}-\d{2}-\d{2}$'
        pattern_telefono = r'^\d{1,10}$'
        pattern_sesso = r'^(uomo|donna)$'
        pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        pattern_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'

        # Validazione con le regex
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

        if conn:
            try:
                user = Utente(
                    nome=nome,
                    cognome=cognome,
                    email=email,
                    password=password,
                    sesso=sesso,
                    numero_telefono=telefono,
                    data_nascita=data_nascita)

                user.save()
            except mysql.connector.Error as err:
                print(f"Errore durante l'esecuzione della query: {err}")
            finally:
                cursor.close()
                conn.close()

        return redirect(url_for('login'))

    return render_template('registrazione.html')
