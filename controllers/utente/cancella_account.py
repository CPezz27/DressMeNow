from flask import Flask, session, redirect, url_for, Blueprint
from utils import mysql_config
from models import Utente
import mysql.connector

app = Flask(__name__)

conn = mysql_config.get_database_connection()
cursor = conn.cursor()

app_bp = Blueprint('delete_account', __name__)


@app_bp.route('/delete_account', methods=['POST'])
def delete_account():

    if 'id' not in session:
        return redirect('utente/login')

    try:
        user_id = session['id']
        Utente.delete_account(user_id)

        session.pop('id', None)
        session.pop('logged_in', None)

        return redirect(url_for('homepage'))

    except mysql.connector.Error as err:
        print(f"Errore durante la cancellazione dell'account: {err}")
        return redirect(url_for('profilo', message='Si è verificato un errore'))

    finally:
        cursor.close()
        conn.close()