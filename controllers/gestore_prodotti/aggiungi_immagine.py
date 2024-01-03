from flask import Blueprint, render_template, request
from models.Immagine import Immagine
from models import Immagine

app_bp = Blueprint('image_controller', __name__)

TIPO_IMMAGINE = 'avatar', 'pagina_prodotto'


@app_bp.route("/aggiungi_immagine", methods=['GET', 'POST'])
def aggiungi_immagine():
    if request.method == 'POST':
        id_prodotto = request.form['id_prodotto']
        immagine = request.files['immagine']

        Immagine.salva_immagine(id_prodotto, immagine, TIPO_IMMAGINE)

        return render_template("dettaglio_prodotto.html", id_prodotto=id_prodotto)

    return render_template("aggiungi_immagine.html")
