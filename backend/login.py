import re
from flask import Flask, render_template, request, redirect, session, url_for
import logging
import mysql.connector

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your_secret_key'  # Chiave segreta per gestire le sessioni

logging.basicConfig(level=logging.DEBUG)

def is_valid_password(password):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'
    return re.match(regex, password) is not None

# Connessione al database MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Carlodi02",
    database="DressMeNow"
)

mycursor = mydb.cursor()

@app.route('/')
def login_page():
    return render_template('login.html')


# Pagina di login
@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not is_valid_password(password):
            error_message = "La password non rispetta i criteri richiesti."
            return render_template('login.html', error_message=error_message)

        # Verifica delle credenziali nel database
        sql = "SELECT * FROM utente WHERE email = %s AND password = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        if user:
            # Creazione della sessione
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('profilo', email=email))
        else:
            return "Credenziali non valide. Riprova."

    return redirect('Profilo.html')

@app.route("/profilo/<email>")
def profilo(email):
    return render_template("Profilo.html", email=email)


# Pagina del dashboard dopo il login
    #@app.route('/AreaRiservata')
    #def dashboard():
    #    if 'logged_in' in session:
    #        return f"Benvenuto, {session['email']}! Questa è la tua area riservata."
    #    else:
    #        return redirect('/login')


# Pagina di logout
#@app.route('/logout')
#def logout():
#    session.pop('logged_in', None)
#    session.pop('email', None)
#    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)