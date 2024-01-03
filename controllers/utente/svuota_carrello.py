from flask import Blueprint, request

from models.Carrello import svuota_carrello

app_bp = Blueprint('svuota_carrello', __name__)

@app_bp.route("/svuota_carrello", methods=['POST'])
def svuota_carrello_controller():
    try:
        id_carrello = request.json.get('id_carrello')

        svuota_carrello(id_carrello)

        return {"message": "Carrello svuotato con successo."}
    except Exception as e:
        # Gestisci gli errori in modo adeguato
        return {"error": str(e)}
