from models.Taglia import Taglia
from flask import Blueprint, render_template


app_bp = Blueprint('aggiungi_taglia', __name__)


@app_bp.route("/aggiungi_taglia", methods=['POST'])
def aggiungi_taglia(nome_taglia):
    if aggiungi_taglia(nome_taglia):
        return render_template("success.html", message="Taglia aggiunta correttamente.")
    else:
        return None
