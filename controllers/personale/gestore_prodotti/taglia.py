from flask import Blueprint, render_template, redirect, request
from models.Taglia import Taglia
from models import Taglia

app_bp = Blueprint('user_prodotti', __name__)


@app_bp.route("/aggiungi_taglia", methods=['POST'])
def aggiungi_taglia():
    if request.method == 'POST':
        nome_taglia = request.form['nome_taglia']
        success = Taglia(nome_taglia=nome_taglia).save()
        if success:
            return redirect("utente/index.html")  # Reindirizza alla pagina principale o ad una pagina di conferma
        else:
            return render_template("errore.html")  # Mostra una pagina di errore
    else:
        return redirect("utente/index.html")  # Se non viene inviato un metodo POST, reindirizza alla pagina principale


@app_bp.route("/modifica_taglia", methods=['POST'])
def modifica_taglia():
    if request.method == 'POST':
        id_taglia = request.form['id_taglia']
        nome_taglia = request.form['nome_taglia']
        taglia = Taglia(id_taglia=id_taglia, nome_taglia=nome_taglia)
        success = taglia.save()
        if success:
            return redirect("utente/index.html")
        else:
            return render_template("errore.html")
    else:
        return redirect("utente/index.html")


@app_bp.route("/rimuovi_taglia", methods=['POST'])
def rimuovi_taglia():
    if request.method == 'POST':
        id_taglia = request.form['id_taglia']
        success = Taglia.rimozione_taglia(id_taglia)
        if success:
            return redirect("utente/index.html")
        else:
            return render_template("errore.html")
    else:
        return redirect("utente/index.html")

