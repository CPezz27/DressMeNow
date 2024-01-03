from flask import Blueprint, render_template
from models import Ordine, ProdottoInOrdine
from models.ProdottoInOrdine import ProdottoInOrdine

app_bp = Blueprint('user_statistiche_ordine', __name__)


@app_bp.route("/statistiche_ordini")
def visualizza_statistiche_ordini():
    try:
        vendite_totali = Ordine.calcola_vendite_totali()

        guadagno = Ordine.calcola_guadagno()

        prodotti_resi = ProdottoInOrdine.conta_prodotti_resi()

        percentuale_resi = ProdottoInOrdine.percentuale_prodotti_resi()

        return render_template("utente/statistiche_ordini.html",
                               vendite_totali=vendite_totali,
                               guadagno=guadagno,
                               prodotti_resi=prodotti_resi,
                               percentuale_resi=percentuale_resi)
    except Exception as e:
        return render_template("errore.html", message="Errore durante il recupero delle statistiche ordini.")
