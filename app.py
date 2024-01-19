from flask import Flask
from controllers import index
from controllers.utente import login, profilo, registrati, effettua_ordine, carrello, prodotti, indirizzi, pagamenti, avatar, ricercaNLP
from controllers.personale import login as login_personale
from controllers.personale.direttore import direttore
from controllers.personale.gestore_prodotti import prodotti as prodotti_gestore, taglia, immagini
from controllers.personale.gestore_ordini import ordini


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(index.app_bp)
app.register_blueprint(login.app_bp)
app.register_blueprint(login_personale.app_bp)
app.register_blueprint(profilo.app_bp)
app.register_blueprint(registrati.app_bp)
app.register_blueprint(effettua_ordine.app_bp)
app.register_blueprint(carrello.app_bp)
app.register_blueprint(prodotti.app_bp)
app.register_blueprint(prodotti_gestore.app_bp)
app.register_blueprint(direttore.app_bp)
app.register_blueprint(ordini.app_bp)
app.register_blueprint(taglia.app_bp)
app.register_blueprint(indirizzi.app_bp)
app.register_blueprint(immagini.app_bp)
app.register_blueprint(ricercaNLP.app_bp)
app.register_blueprint(pagamenti.app_bp)
app.register_blueprint(avatar.app_bp)


if __name__ == '__main__':
    app.run(debug=True)
