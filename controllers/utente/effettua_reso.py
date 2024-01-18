from flask import Blueprint, render_template, request, session, redirect, url_for

from models import Ordine

app_bp = Blueprint('effettua_reso', __name__)


@app_bp.route('/o/effettua_reso', methods=['POST'])
def effettua_reso():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    if request.method == 'POST':
        try:
            order_id = request.form.get('id_ordine')
            note_reso = request.form.get('note_reso')

            if Ordine.modifica_reso( 'Reso richiesto', note_reso, order_id):
                return redirect(url_for('effettua_reso.reso_ordine', order_id=order_id, message='Reso richiesto con successo'))
            else:
                return redirect(url_for('effettua_reso.reso_ordine'), order_id=order_id, message='Errore durante la richiesta del reso')

        except Exception as err:
            return redirect(url_for('effettua_reso.reso_ordine'), order_id=order_id, message=f'Errore durante il reso: {err}')

    return redirect(url_for('effettua_reso.reso_ordine'), order_id=order_id, message='Il metodo non è accessibile')


@app_bp.route('/o/reso_ordine/<int:order_id>', methods=['GET', 'POST'])
def reso_ordine(order_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    print("\n\nECCOMI\n\n")
    try:
        print("OOOOOOO")
        data = Ordine.visualizza_ordine_conimg(order_id)
        print(str(data))

        if data:
            return render_template('/utente/resoOrdine.html', data=data)
        else:
            return render_template('/utente/resoOrdine.html', message='Errore durante il reso')

    except Exception as err:
        return render_template('/utente/resoOrdine.html', message=f'Errore durante il reso: {err}')

    return render_template('/utente/resoOrdine.html', message='Il metodo non è accessibile')
