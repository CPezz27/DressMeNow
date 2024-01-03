from flask import Blueprint, render_template
from models.Immagine import Immagine

app_bp = Blueprint('image_controller', __name__)


@app_bp.route("/rimuovi_immagine/<int:id_immagine>", methods=['POST'])
def rimuovi_immagine(id_immagine):

    Immagine.rimuovi_immagine(id_immagine)

    return render_template("dettaglio_prodotto.html")
