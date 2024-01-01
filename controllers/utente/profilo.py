from flask import Blueprint, render_template

app_bp = Blueprint('user', __name__)


@app_bp.route("/profilo")
def profilo():
    return render_template("profilo.html")
