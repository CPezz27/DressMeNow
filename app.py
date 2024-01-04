from flask import Flask
from controllers.utente import login, profilo, registrati, effettua_ordine, carrello, prodotti

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(login.app_bp)
app.register_blueprint(profilo.app_bp)
app.register_blueprint(registrati.app_bp)
app.register_blueprint(effettua_ordine.app_bp)
app.register_blueprint(carrello.app_bp)
app.register_blueprint(prodotti.app_bp)

if __name__ == '__main__':
    app.run(debug=True)
