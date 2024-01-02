from flask import Flask, render_template, redirect, url_for, session

import mysql.connector
from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Utente
from utils import mysql_config
from utils.utils import is_valid_password

@app.route('/confirm_delete_account')
def confirm_delete_account():
    return render_template('/profilo')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'id' in session and session['logged_in']:

        db.execute("DELETE FROM Utente WHERE id = ?", (session['id'],))

        session.pop('id', None)
        session.pop('logged_in', None)

        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login'))


# Pagina di conferma della cancellazione dell'account
@app.route('/account_deleted')
def account_deleted():
    return "Il tuo account è stato cancellato con successo."


if __name__ == '__main__':
    app.run(debug=True)
