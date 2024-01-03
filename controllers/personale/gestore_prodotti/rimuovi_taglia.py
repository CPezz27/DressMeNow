from models.Taglia import Taglia
from flask import Blueprint, render_template


app_bp = Blueprint('rimuovi_taglia', __name__)


@app_bp.route("/rimuovi_taglia", methods=['POST'])
def rimuovi_taglia(nome_taglia):
    if rimuovi_taglia(nome_taglia):
        return render_template("success.html", message="Taglia rimossa correttamente.")
    else:
        return None
