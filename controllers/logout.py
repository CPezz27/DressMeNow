from flask import Blueprint, session, redirect, url_for

from utils import mysql_config

app_bp = Blueprint('user_logout', __name__)


@app_bp.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('logged_in', None)
    return redirect(url_for('homepage'))
