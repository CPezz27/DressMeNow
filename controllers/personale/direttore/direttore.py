from flask import Blueprint, render_template
from models.Utente import Utente

app_bp = Blueprint('user_controller', __name__)


@app_bp.route("/d/")
def visualizza_personale():
    utenti = Utente.visualizza_tutti_gli_utenti()

    if not utenti:
        return render_template("errore.html", message="Si è verificato un errore durante il recupero degli utenti.")

    return render_template("lista_utenti.html", utenti=utenti)


@app_bp.route("/d/aggiungi_personale")
def aggiungi_personale():
    utenti = Utente.visualizza_tutti_gli_utenti()

    if not utenti:
        return render_template("errore.html", message="Si è verificato un errore durante il recupero degli utenti.")

    return render_template("lista_utenti.html", utenti=utenti)


@app_bp.route("/d/modifica_personale")
def modifica_personale():
    utenti = Utente.visualizza_tutti_gli_utenti()

    if not utenti:
        return render_template("errore.html", message="Si è verificato un errore durante il recupero degli utenti.")

    return render_template("lista_utenti.html", utenti=utenti)


@app_bp.route("/d/rimuovi_personale")
def rimuovi_personale():
    utenti = Utente.visualizza_tutti_gli_utenti()

    if not utenti:
        return render_template("errore.html", message="Si è verificato un errore durante il recupero degli utenti.")

    return render_template("lista_utenti.html", utenti=utenti)
