from flask import Flask, render_template, request, redirect, session, url_for
import logging
import mysql.connector

app = Flask(__name__, template_folder='../../../../templates', static_folder='../../../../static')
app.secret_key = 'your_secret_key'  # Chiave segreta per gestire le sessioni

logging.basicConfig(level=logging.DEBUG)

# Connessione al database MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="DressMeNow"
)

mycursor = mydb.cursor()

@app.route('/')
def login_page():
    return render_template('loginAdmin.html')


# Pagina di login dell'amministratore
@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica delle credenziali nel database
        sql = "SELECT * FROM personale WHERE email = %s AND password = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        if user:
            # Creazione della sessione
            session['logged_in'] = True
            session['email'] = email

            tipo_personale = user[3]

            # Redirect in base al tipo di personale
            if tipo_personale == 'direttore':
                return redirect(url_for('direttore'))
            elif tipo_personale == 'gestore_ordine':
                return redirect(url_for('gestore_ordine'))
            elif tipo_personale == 'gestore_prodotto':
                return redirect(url_for('gestore_prodotto'))


        else:
            return "Credenziali non valide. Riprova."

@app.route('/gestore_ordine')
def gestore_ordine():
    return render_template('gestoreOrdine.html')

@app.route('/gestore_prodotto')
def gestore_prodotto():
    return render_template('gestoreProdotto.html')

@app.route('/direttore')
def direttore():
    return render_template('direttore.html')


if __name__ == '__main__':
    app.run(debug=True)