from flask import Blueprint, request

from models.Carrello import aggiungi_al_carrello

app_bp = Blueprint('aggiungi_al_carrello', __name__)

@app_bp.route("/aggiungi_al_carrello", methods=['POST'])
def aggiungi_al_carrello_controller():
    try:
        id_carrello = request.json.get('id_carrello')
        id_prodotto = request.json.get('id_prodotto')
        quantita = request.json.get('quantita', 1)

        aggiungi_al_carrello(id_carrello, id_prodotto, quantita)

        return {"/prodotto.html"}
    except Exception as e:
        return {"error": str(e)}
