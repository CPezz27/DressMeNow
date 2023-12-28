pip install Flask
pip install mysql-connector-python

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="nome_del_database"
)

mycursor = mydb.cursor()

#Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect('/index.html')

    return render_template('register.html')


# Valid Registration
@app.route('/registration_successful')
def registration_successful():
    return 'Registrazione completata!'


if __name__ == '__main__':
    app.run(debug=True)
