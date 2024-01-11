import mysql.connector
from flask import Blueprint, render_template, request, redirect, session, url_for

from models import Personale
from models import Prodotto
from utils import mysql_config

app_bp = Blueprint('direttore_login', __name__)

conn = mysql_config.get_database_connection()

cursor = conn.cursor()


@app_bp.route('/direttore/login')
def login_page():
    return render_template('direttore/login.html')


@app_bp.route('/direttore/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if conn:
            try:
                direttore = Personale.login(email, password)

                if direttore:
                    session['logged_in'] = True
                    session['email'] = email

                    tipo_personale = direttore[3]

                    if tipo_personale == 'direttore':
                        session['ruolo'] = 'direttore'
                        return redirect(url_for('direttore_controller.visualizza_personale'))
                    elif tipo_personale == 'gestore_ordine':
                        session['ruolo'] = 'gestore_ordine'
                        return redirect(url_for('order_controller.dashboard'))
                    elif tipo_personale == 'gestore_prodotto':
                        session['ruolo'] = 'gestore_prodotto'
                        return redirect(url_for('direttore_login.gestore_prodotto'))
                else:
                    return "Credenziali non valide. Riprova."
            except mysql.connector.Error as err:
                print(f"Errore durante l'esecuzione della query")
            finally:
                cursor.close()
                conn.close()


@app_bp.route('/gestore_ordine')
def gestore_ordine():
    return render_template('gestoreOrdine.html')


@app_bp.route('/gestore_prodotto')
def gestore_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))
    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))
    try:
        prodotti_tutti = Prodotto.view_products()
        prodotti_dict = {}
        for prodotto in prodotti_tutti:
            prodotto_id = prodotto[0]
            if prodotto_id not in prodotti_dict:
                prodotti_dict[prodotto_id] = {
                    'id_prodotto': prodotto[0],
                    'nome': prodotto[1],
                    'categoria': prodotto[2],
                    'marca': prodotto[3],
                    'descrizione': prodotto[4],
                    'vestibilita': prodotto[5],
                    'prezzo': float(prodotto[6]),  # Converti il prezzo in float se necessario
                    'colore': prodotto[7],
                    'materiale': prodotto[8],
                    'taglie': []  # Lista vuota per le taglie
                }
                
            # Recupera le taglie associate al prodotto
            taglie_prodotto = Prodotto.get_sizes_for_product(prodotto_id)  # Sostituisci con il metodo corretto
            for taglia in taglie_prodotto:

                prodotti_dict[prodotto_id]['taglie'].append({
                    'id_taglia': taglia[0],
                    'nometaglia': taglia[1],
                    'quantita': taglia[2]
                })
        prodotti_finali = list(prodotti_dict.values())
        print("test1")        
        return render_template('gestoreProdotto.html', prodotti_da_mostrare=prodotti_finali)
    except Exception as err:
        print(err)
        return render_template('/direttore/login.html', messaggio="Errore durante la visualizzazione")

