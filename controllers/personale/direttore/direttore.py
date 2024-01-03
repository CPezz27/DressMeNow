from flask import Blueprint, render_template, request
from models import Personale
from models.Personale import Personale

app_bp = Blueprint('user_controller', __name__)


@app_bp.route("/d/")
def visualizza_personale():
    personale = Personale.get_all_personale()
    return render_template("direttore/personale.html", data=personale)


@app_bp.route("/d/aggiungi_personale", methods=['GET', 'POST'])
def aggiungi_personale():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tipo_personale = request.form['tipo_personale']
        personale = Personale(
            email=email,
            password=password,
            tipo_personale=tipo_personale
        )
        flag = personale.save()
        if flag:
            return render_template("direttore/personale.html", message="Personale creato correttamente.")
        else:
            return render_template("direttore/personale.html", message="Personale non creato.")

    return render_template("direttore/aggiungi_personale.html")


@app_bp.route("/d/modifica_personale", methods=['GET', 'POST'])
def modifica_personale():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tipo_personale = request.form['tipo_personale']
        flag = Personale.update_personale(email, password, tipo_personale)
        if flag:
            return render_template("direttore/modifica_personale.html", message="Personale modificato correttamente.")
        else:
            return render_template("direttore/modifica_personale.html", message="Personale non modificato.")

    return render_template("direttore/modifica_personale.html")


@app_bp.route("/d/rimuovi_personale", methods=['POST'])
def rimuovi_personale():
    if request.method == 'POST':
        id_personale = request.form['id_personale']
        flag = Personale.delete_personale(id_personale)
        if flag:
            return render_template("direttore/personale.html", message="Personale rimosso correttamente.")
        else:
            return render_template("direttore/personale.html", message="Personale non rimosso.")
