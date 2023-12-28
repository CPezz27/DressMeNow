from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Chiave segreta per gestire le sessioni

# Connessione al database MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="nome_del_database"
)

mycursor = mydb.cursor()


# Pagina di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica delle credenziali nel database
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        if user:
            # Creazione della sessione
            session['logged_in'] = True
            session['username'] = username
            return redirect('/dashboard')  # Redirect alla pagina del dashboard dopo il login
        else:
            return "Credenziali non valide. Riprova."

    return render_template('login.html')


# Pagina del dashboard dopo il login
@app.route('/AreaRiservata')
def dashboard():
    if 'logged_in' in session:
        return f"Benvenuto, {session['username']}! Questa è la tua area riservata."
    else:
        return redirect('/login')


# Pagina di logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
