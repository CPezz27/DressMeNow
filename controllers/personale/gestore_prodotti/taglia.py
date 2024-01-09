from flask import Blueprint, render_template, redirect, request, session, url_for

from models import Taglia
from models.Taglia import Taglia as TagliaClass

app_bp = Blueprint('taglia_controller', __name__)

@app_bp.route('/aggiunta_taglia')
def aggiunta_taglia():
    id_prodotto = request.args.get('id_prodotto')

    #voglio vedere quali taglie sono state già aggiunte per questo prodotto:
    taglie_impostate = Taglia.get_taglie_quantita_by_id_prodotto(id_prodotto)

    #ora voglio vedere quali sono le taglie disponibili nel DB:
    taglie_disponibili = Taglia.get_elenco_taglie()

    return render_template('aggiungiTaglia.html', id_prodotto = id_prodotto, taglie_impostate = taglie_impostate, taglie_disponibili = taglie_disponibili)


@app_bp.route("/gp/aggiungi_taglia", methods=['POST'])
def aggiungi_taglia():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome_taglia = request.form['nome_taglia']
        taglia = Taglia(nome_taglia=nome_taglia)
        success = taglia.save()
        if success:
            return redirect("utente/index.html")  # Reindirizza alla pagina principale o ad una pagina di conferma
        else:
            return render_template("errore.html")  # Mostra una pagina di errore
    else:
        return redirect("utente/index.html")  # Se non viene inviato un metodo POST, reindirizza alla pagina principale
    

    

@app_bp.route("/gp/aggiungi_taglia_al_prodotto", methods=['POST'])
def aggiungi_taglia_al_prodotto():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        quantita = request.form['qta']
        id_taglia = request.form['taglia']
        id_prodotto = request.form['id_prodotto']
        #taglia = Taglia(nome_taglia=nome_taglia)
        success = Taglia.inserisci_taglia_prodotto_nel_database(id_taglia, id_prodotto, quantita)

        if success:
            return redirect(url_for('taglia_controller.aggiunta_taglia', id_prodotto=id_prodotto))
        else:
            return render_template("errore.html")  # Mostra una pagina di errore
    else:
        return redirect("utente/index.html")  # Se non viene inviato un metodo POST, reindirizza alla pagina principale


@app_bp.route("/gp/modifica_taglia", methods=['POST'])
def modifica_taglia():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_taglia = request.form['id_taglia']
        nome_taglia = request.form['nome_taglia']
        success = Taglia.modifica_taglia(id_taglia=id_taglia, nome_taglia=nome_taglia)
        if success:
            return redirect("utente/index.html")
        else:
            return render_template("errore.html")
    else:
        return redirect("utente/index.html")


@app_bp.route("/gp/rimuovi_taglia", methods=['POST'])
def rimuovi_taglia():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if session['ruolo'] != 'gestore_prodotto':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_taglia = request.form['id_taglia']
        success = Taglia.rimozione_taglia(id_taglia)
        if success:
            return redirect("utente/index.html")
        else:
            return render_template("errore.html")
    else:
        return redirect("utente/index.html")
