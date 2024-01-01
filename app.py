from flask import Flask
from controllers.utente import login, profilo, registrati

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(login.app_bp)
app.register_blueprint(profilo.app_bp)
app.register_blueprint(registrati.app_bp)

if __name__ == '__main__':
    app.run(debug=True)
