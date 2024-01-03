from flask import Blueprint, render_template, request
from models import Ordine


app_bp = Blueprint('order_controller', __name__)


@app_bp.route("/cancella_ordine", methods=['POST'])
def cancella_ordine():
    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        success = cancella_ordine(id_ordine)

        if success:
            return render_template("success.html", message="Ordine cancellato correttamente.")
        else:
            return render_template("error.html", message="Errore durante la cancellazione dell'ordine.")


@app_bp.route("/modifica_stato_ordine", methods=['POST'])
def modifica_stato_ordine():
    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        nuovo_stato = request.form['nuovo_stato']
        success = modifica_stato_ordine(id_ordine, nuovo_stato)

        if success:
            return render_template("success.html", message="Stato dell'ordine modificato correttamente.")
        else:
            return render_template("error.html", message="Errore durante la modifica dello stato dell'ordine.")


@app_bp.route("/modifica_ordine", methods=['POST'])
def modifica_ordine():
    if request.method == 'POST':
        id_ordine = request.form['id_ordine']
        nuovo_stato = request.form['nuovo_stato']

        success = Ordine.modifica_ordine(id_ordine, nuovo_stato)

        if success:
            return render_template("successo.html", message="Stato dell'ordine modificato con successo.")
        else:
            return render_template("errore.html", message="Si è verificato un errore durante la modifica dell'ordine.")