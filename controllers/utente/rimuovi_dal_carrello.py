from flask import Blueprint, request

from models.Carrello import rimuovi_dal_carrello

app_bp = Blueprint('rimuovi_dal_carrello', __name__)

@app_bp.route("/rimuovi_dal_carrello", methods=['POST'])
def rimuovi_dal_carrello_controller():
    try:
        id_carrello = request.json.get('id_carrello')
        id_prodotto = request.json.get('id_prodotto')

        rimuovi_dal_carrello(id_carrello, id_prodotto)

        return {"message": "Prodotto rimosso dal carrello con successo."}
    except Exception as e:
        return {"error": str(e)}
