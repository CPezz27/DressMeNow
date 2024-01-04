from flask import Blueprint, session, redirect, url_for

app_bp = Blueprint('user_logout', __name__)


@app_bp.route('/logout')
def logout():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('user_login.login_page'))

    session.pop('id', None)
    session.pop('logged_in', None)
    return redirect(url_for('homepage'))
