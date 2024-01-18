from flask import Blueprint, render_template, redirect, request, session, url_for

from models.ConfigurazioneAvatar import update_configurazione_avatar

app_bp = Blueprint('user_avatar', __name__)


@app_bp.route('/modifica_avatar', methods=['POST'])
def modifica_avatar():
    user_id = session.get('id')
    if user_id:
        nuovi_valori = {
            'colore_pelle': request.form.get('colorePelle'),
            'colore_occhi': request.form.get('coloreOcchi'),
            'colore_capelli': request.form.get('coloreCapelli'),
            'lunghezza_capelli': request.form.get('lunghezzaCapelli'),
            'altezza': request.form.get('altezza'),
            'peso': request.form.get('peso'),
            'barba': request.form.get('barba'),
            'eta': request.form.get('eta'),
            'dimensioniCorpo': request.form.get('dimensioniCorpo'),
            'sesso': request.form.get('sesso'),
        }
        config_avatar = {
            'colore_pelle': nuovi_valori['colore_pelle'],
            'colore_occhi': nuovi_valori['colore_occhi'],
            'colore_capelli': nuovi_valori['colore_capelli'],
            'lunghezza_capelli': nuovi_valori['lunghezza_capelli'],
            'altezza': nuovi_valori['altezza'],
            'peso': nuovi_valori['peso'],
            'barba': nuovi_valori['barba'],
            'eta': nuovi_valori['eta'],
            'dimensioniCorpo': nuovi_valori['dimensioniCorpo'],
            'sesso': nuovi_valori['sesso'],
        }
        update_configurazione_avatar(user_id, **config_avatar)
        return redirect(url_for('user_profile.configura_avatar'))