from flask import Blueprint, render_template, request, redirect, url_for
from models import Ordine

effettua_reso_bp = Blueprint('effettua_reso', __name__)

@effettua_reso_bp.route('/gestore_prodotti/effettua_reso/<int:order_id>/<int:product_id>', methods=['POST'])
def effettua_reso(order_id, product_id):
    if request.method == 'POST':
        motivo_reso = request.form.get('motivo_reso')
        try:
            ordine_da_modificare = Ordine.view_order(order_id)
            id_prodotto = product_id
            ordine_da_modificare.effettua_reso(id_prodotto, motivo_reso)

            return render_template('/gestore_prodotti/effettua_reso.html', message='Reso effettuato con successo')
        except Exception as err:
            return render_template('/gestore_prodotti/effettua_reso.html', error=f'Errore durante l\'effettuazione del reso: {err}')

    return render_template('/gestore_prodotti/effettua_reso.html', error='Il metodo è accessibile solo tramite richieste POST')
