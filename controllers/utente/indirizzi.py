from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Indirizzo
from models.Indirizzo import Indirizzo, get_address, get_addresses, update, delete
from controllers.utente.profilo import indirizzi
from utils.utils import validate_input

app_bp = Blueprint('gestione_indirizzi', __name__)


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

            new_address = Indirizzo(
                id_utente=user_id, provincia=provincia, cap=cap, via=via, tipo=tipo, citta=citta)
            success = new_address.save()
            if success:
                return redirect(url_for('user_profile.indirizzi'))
            else:
                return render_template('errore.html', message="Errore durante l'aggiunta dell'indirizzo.")
        else:
            return render_template('/login')

    return render_template('utente/aggiungi_indirizzo.html')


@app_bp.route('/indirizzo/modifica/<int:address_id>', methods=['POST'])
def modifica_indirizzo(address_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        user_id = session.get('id')
        if user_id:
            provincia = request.form.get('provincia')
            cap = request.form.get('cap')
            via = request.form.get('via')
            tipo = request.form.get('tipo')
            citta = request.form.get('citta')

            address = get_address(address_id)
            if address and address[1] == user_id:
                success = update(provincia, cap, via, tipo, citta, address_id)
                if success:
                    return redirect(url_for('user_profile.indirizzi'))
                else:
                    return render_template('errore.html', message="Errore durante la modifica dell'indirizzo.")
            else:
                return render_template('404.html', message="Indirizzo non trovato o non autorizzato.")
        else:
            return redirect(url_for('user_login.login_page'))


@app_bp.route('/indirizzo/elimina/<int:address_id>', methods=['GET'])
def elimina_indirizzo(address_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session.get('id')
    print("\n\n\nid indirizzo: ", address_id)
    print("\n\n\nid utente: ", user_id)
    address_id = int(address_id)
    if user_id:
        print("Ho superato il 1 if:", address_id, user_id)
        address = get_address(address_id)
        print("\n\n\n\n oliooooo", str(address))
        if address and address[1] == user_id:
            success = delete(address_id)
            print(success)
            if success:
                print("Sono nel successo!!!!")
                print(url_for('user_profile.indirizzi'))
                return redirect(url_for('user_profile.indirizzi'))
            else:
                return render_template('errore.html', message="Errore durante l'eliminazione dell'indirizzo.")
        else:
            return render_template('404.html', message="Indirizzo non trovato o non autorizzato.")
    else:
        return redirect(url_for('user_login.login_page'))
