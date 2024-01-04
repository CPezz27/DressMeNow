from flask import Blueprint, render_template, request
from models import Ordine

app_bp = Blueprint('effettua_reso', __name__)


@app_bp.route('/o/effettua_reso', methods=['POST'])
def effettua_reso():
    if request.method == 'POST':
        try:
            id_ordine = request.form.get('id_ordine')
            id_prodotto = request.form.get('id_prodotto')
            note_reso = request.form.get('note_reso')

            if Ordine.modifica_reso(id_prodotto, 'richiesto', note_reso, id_ordine):
                return render_template('/gestore_prodotti/effettua_reso.html', message='Reso effettuato con successo')
            else:
                return render_template('/gestore_prodotti/effettua_reso.html', error='Errore durante il reso')

        except Exception as err:
            return render_template('/gestore_prodotti/effettua_reso.html', error=f'Errore durante il reso: {err}')

    return render_template('/gestore_prodotti/effettua_reso.html', error='Il metodo non è accessibile')
