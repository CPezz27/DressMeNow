from flask import Flask, render_template, request, redirect, url_for
from connessione import MySQLDatabase
import re
import hashlib

app = Flask(__name__)

db = MySQLDatabase()

# Funzione di validazione con regex
def validate_input(data, pattern):
    return re.match(pattern, data)

def hash_password_sha256(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

# Pagina di registrazione
@app.route('/')
def registrazione():
    return render_template('registrazione.html')

# Endpoint per gestire la registrazione
@app.route('/registrati', methods=['POST'])
def registrati():
    if request.method == 'POST':
        nome = request.form['firstName']
        cognome = request.form['lastName']
        data_nascita = request.form['dataNascita']
        telefono = request.form['NumeroTelefonico']
        sesso = request.form['sesso']
        email = request.form['email']
        password = request.form['confirmPassword']

        
        print(data_nascita)
        
        
        
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


        hashed_password = hash_password_sha256(password)
        
        # Inserimento dati nel database
        db.insert_data(table='utente', data={
            'nome': nome,
            'cognome': cognome,
            'email': email,
            'password': hashed_password,
            'data_nascita': data_nascita, 
            'telefono': telefono,
            'sesso': sesso  
        })

        db.close_connection()
        return redirect(url_for('pagina_di_conferma'))

@app.route('/conferma')
def pagina_di_conferma():
    return 'Registrazione completata con successo!'

if __name__ == '__main__':
    app.run(debug=True)
