from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Indirizzo
from models.Indirizzo import Indirizzo
from utils.utils import validate_input

app_bp = Blueprint('gestione_indirizzi', __name__)


@app_bp.route('/indirizzi', methods=['GET'])
def visualizza_indirizzi():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session.get('id')
    if user_id:
        addresses = Indirizzo.get_addresses(user_id)
        return render_template('indirizzi.html', addresses=addresses)
    else:
        return render_template('/login')


@app_bp.route('/indirizzo/aggiungi', methods=['GET', 'POST'])
def aggiungi_indirizzo():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            provincia = request.form['provincia']
            cap = request.form['cap']
            via = request.form['via']
            tipo = request.form['tipo']
            citta = request.form['citta']

            pattern_provincia = r'^[A-Za-z ]+$'
            pattern_cap = r'^\d{5}$'
            pattern_via = r'^[A-Za-z0-9 ]+$'
            pattern_tipo = r'^(Spedizione|Fatturazione)$'
            pattern_citta = r'^[A-Za-z ]+$'

            if not all([
                validate_input(provincia, pattern_provincia),
                validate_input(cap, pattern_cap),
                validate_input(via, pattern_via),
                validate_input(tipo, pattern_tipo),
                validate_input(citta, pattern_citta)
            ]):
                return "Dati inseriti non validi. Controlla i campi e riprova."

            new_address = Indirizzo(id_utente=user_id, provincia=provincia, cap=cap, via=via, tipo=tipo, citta=citta)
            success = new_address.save()
            if success:
                return redirect(url_for('gestione_indirizzi.visualizza_indirizzi'))
            else:
                return render_template('errore.html', message="Errore durante l'aggiunta dell'indirizzo.")
        else:
            return render_template('/login')

    return render_template('aggiungi_indirizzo.html')


@app_bp.route('/indirizzo/modifica/<int:address_id>', methods=['GET', 'POST'])
def modifica_indirizzo(address_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            provincia = request.form['provincia']
            cap = request.form['cap']
            via = request.form['via']
            tipo = request.form['tipo']
            citta = request.form['citta']

            pattern_provincia = r'^[A-Za-z ]+$'
            pattern_cap = r'^\d{5}$'
            pattern_via = r'^[A-Za-z0-9 ]+$'
            pattern_tipo = r'^(Spedizione|Fatturazione)$'
            pattern_citta = r'^[A-Za-z ]+$'

            if not all([
                validate_input(provincia, pattern_provincia),
                validate_input(cap, pattern_cap),
                validate_input(via, pattern_via),
                validate_input(tipo, pattern_tipo),
                validate_input(citta, pattern_citta)
            ]):
                return "Dati inseriti non validi. Controlla i campi e riprova."

            address = Indirizzo.get_address(address_id)
            if address and address.id_utente == user_id:
                address.provincia = provincia
                address.cap = cap
                address.via = via
                address.tipo = tipo
                address.citta = citta
                success = address.save()
                if success:
                    return redirect(url_for('gestione_indirizzi.visualizza_indirizzi'))
                else:
                    return render_template('errore.html', message="Errore durante la modifica dell'indirizzo.")
            else:
                return render_template('404.html', message="Indirizzo non trovato o non autorizzato.")
        else:
            return render_template('/login')

    address = Indirizzo.get_address(address_id)
    if address:
        return render_template('modifica_indirizzo.html', address=address)
    else:
        return render_template('404.html', message="Indirizzo non trovato.")


@app_bp.route('/indirizzo/elimina/<int:address_id>', methods=['GET'])
def elimina_indirizzo(address_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session.get('id')
    if user_id:
        address = Indirizzo.get_address(address_id)
        if address and address.id_utente == user_id:
            success = Indirizzo.delete(address_id)
            if success:
                return redirect(url_for('gestione_indirizzi.visualizza_indirizzi'))
            else:
                return render_template('errore.html', message="Errore durante l'eliminazione dell'indirizzo.")
        else:
            return render_template('404.html', message="Indirizzo non trovato o non autorizzato.")
    else:
        return redirect(url_for('user_login.login_page'))
