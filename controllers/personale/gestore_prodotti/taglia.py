from models import Taglia
from flask import Blueprint, render_template


app_bp = Blueprint('controller_taglia', __name__)


@app_bp.route("/rimozione_taglia", methods=['POST'])
def rimuovozione_taglia(nome_taglia):
    if rimuovozione_taglia(nome_taglia):
        return render_template("success.html", message="Taglia rimossa correttamente.")
    else:
        return None


@app_bp.route("/aggiungi_taglia", methods=['POST'])
def aggiungi_taglia(nome_taglia):
    if aggiungi_taglia(nome_taglia):
        return render_template("success.html", message="Taglia aggiunta correttamente.")
    else:
        return None
