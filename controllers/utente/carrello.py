from flask import Blueprint, render_template

app_bp = Blueprint('utente_carrello', __name__)


@app_bp.route('/carrello')
def carrello():
    return render_template('/utente/carrello.html')
