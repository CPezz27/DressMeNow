from flask import Blueprint, redirect, render_template, request, session, url_for
from models.Carrello import Carrello

from models.ConfigurazioneAvatar import ConfigurazioneAvatar, update_configurazione_avatar
from models import ConfigurazioneAvatar as CFGAvatar
from models import Carrello

app_bp = Blueprint('user_avatar', __name__)


@app_bp.route('/modifica_avatar', methods=['POST'])
def modifica_avatar():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    user_id = session.get('id')
    nuovi_valori = {
        'colore_pelle': request.form.get('colorePelle'),
        'colore_occhi': request.form.get('coloreOcchi'),
        'colore_capelli': request.form.get('coloreCapelli'),
        'lunghezza_capelli': request.form.get('lunghezzaCapelli'),
        'altezza': request.form.get('altezza'),
        'peso': request.form.get('peso'),
        'barba': request.form.get('barba') == 'on',
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
        'dimensioni_corpo': nuovi_valori['dimensioniCorpo'],
        'sesso': nuovi_valori['sesso'],
    }

    success, rowsAffected = update_configurazione_avatar(
        user_id, **config_avatar)
    if success and rowsAffected > 0:
        return redirect(url_for('user_profile.configura_avatar', message="Modifiche avvenute con successo"))
    elif success and rowsAffected == 0:
        return redirect(url_for('user_profile.configura_avatar', message="Nessuna modifica effettuata"))
    else:
        return redirect(url_for('user_profile.configura_avatar', message="Errore nel salvataggio della modifica"))


@app_bp.route('/prova_su_avatar')
def prova_su_avatar():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('utente/login')

    user_id = session['id']

    avatar_data = CFGAvatar.view_avatar(user_id)

    dati_prodotti, prezzo, immagini_avatar = Carrello.contenuto_carrello(user_id)

    #let's check la taglia e associamoci dei valori veri e propri secondo ciò:
    #   145 - taglia S
    #   158 - taglia M
    #   170 - taglia L
    #   183 - taglia XL

    #eccolo il mapping assurdo
    taglia_numerica = {
        'S': 145,
        'M': 158,
        'L': 170,
        'XL': 183
    }

    for i, item in enumerate(dati_prodotti[0]):
        taglia = item[8]  

        if taglia in taglia_numerica:
            dati_prodotti[0][i] = item[:8] + (taglia_numerica[taglia],) + item[9:]
            

    return render_template("utente/provaSuAvatar.html", avatar=avatar_data, prodotti=dati_prodotti, immagini_avatar=immagini_avatar)
