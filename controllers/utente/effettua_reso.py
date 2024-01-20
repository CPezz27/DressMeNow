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
                data = Ordine.visualizza_ordine_conimg(order_id)
                return render_template('/utente/resoOrdine.html', data=data, message='Reso richiesto con successo')
            else:
                data = Ordine.visualizza_ordine_conimg(order_id)
                return render_template('/utente/resoOrdine.html', data=data, message='Errore durante la richiesta del reso')

        except Exception as err:
            return redirect(url_for('user_profile.orders', message=f'Errore durante il reso: {err}'))

    return redirect(url_for('user_profile.orders', message='Il metodo non è accessibile'))


@app_bp.route('/o/reso_ordine/<int:order_id>', methods=['GET', 'POST'])
def reso_ordine(order_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    try:
        data = Ordine.visualizza_ordine_conimg(order_id)

        if data:
            return render_template('/utente/resoOrdine.html', data=data)
        else:
            return render_template('/utente/resoOrdine.html', message='Errore durante il reso')

    except Exception as err:
        return render_template('/utente/resoOrdine.html', message=f'Errore durante il reso: {err}')
