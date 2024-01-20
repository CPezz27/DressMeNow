from flask import Blueprint, render_template, redirect, request, url_for

from models import Prodotto

app_bp = Blueprint('user_prodotti', __name__)


@app_bp.route("/c")
def products_category():
    category = request.args.get('category')

    if category and (category == 'uomo' or category == 'donna' or category == 'bambino'):
        products = Prodotto.view_products_by_category(category)
        return render_template("utente/categoria.html", data=products)
    else:
        return redirect(url_for('index.homepage'))



@app_bp.route("/search")
def search_products():
    product_name = request.args.get('product_name')

    if product_name:
        products = Prodotto.search_prodotto_by_name(product_name)
        return render_template("utente/ricercaProdotto.html", data=products)
    else:
        return redirect(url_for('index.homepage'))


@app_bp.route("/")
def main_products():
    products = Prodotto.view_products()

    return render_template("utente/search_product.html", data=products)


@app_bp.route("/pd")
def view_product():
    product_id = request.args.get('product_id')

    product = Prodotto.view_product(product_id)


    return render_template("utente/dettagliProdotto.html", data=product)
