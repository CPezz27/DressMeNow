from flask import Blueprint, render_template
from models import Prodotto

app_bp = Blueprint('index', __name__)

@app_bp.route('/')
def homepage():
     results_uomo = Prodotto.view_products_by_category("uomo")
     results_donna = Prodotto.view_products_by_category("donna")
     results_bambino = Prodotto.view_products_by_category("bambino")
     return render_template('index.html', res_u = results_uomo, res_d = results_donna, res_b = results_bambino)