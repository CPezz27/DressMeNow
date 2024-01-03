from flask import Blueprint, render_template
from models.Utente import Utente

app_bp = Blueprint('user_controller', __name__)


@app_bp.route("/visualizza_utenti")
def visualizza_utenti():
    utenti = Utente.visualizza_tutti_gli_utenti()

    if not utenti:
        return render_template("errore.html", message="Si è verificato un errore durante il recupero degli utenti.")

    return render_template("lista_utenti.html", utenti=utenti)
