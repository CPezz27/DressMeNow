from flask import Blueprint, render_template, redirect, request, session

from models import ConfigurazioneAvatar

app_bp = Blueprint('user_avatar', __name__)


@app_bp.route("/p/configura_avatar", methods=['POST'])
def configura_avatar():
    if 'id' not in session:
        return redirect('utente/login')

    user_id = session['id']

    if request.method == 'POST':
        data = request.json
        if data:
            success = ConfigurazioneAvatar.update_configurazione_avatar(user_id, **data)
            if success:
                return render_template("utente/avatar.html", message="Avatar aggiornato correttamente.")
            else:
                return render_template("utente/avatar.html", message="Avatar non aggiornato.")
        else:
            return render_template("utente/avatar.html", message="Parametri mancanti.")
