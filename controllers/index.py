from flask import Blueprint, render_template

app_bp = Blueprint('index', __name__)

@app_bp.route('/')
def homepage():
     return render_template('index.html')