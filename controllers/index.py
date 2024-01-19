from flask import Blueprint, render_template
from models import Prodotto

app_bp = Blueprint('index', __name__)


@app_bp.errorhandler(403)
def page_not_found(error):
    return render_template('403.html'), 403


@app_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app_bp.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


@app_bp.route('/')
def homepage():
    results_uomo = Prodotto.view_products_by_category("uomo")[:3]
    results_donna = Prodotto.view_products_by_category("donna")[:3]
    results_bambino = Prodotto.view_products_by_category("bambino")[:3]
    return render_template('index.html', res_u=results_uomo, res_d=results_donna, res_b=results_bambino)
