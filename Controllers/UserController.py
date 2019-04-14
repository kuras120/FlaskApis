import datetime

from flask import render_template, session, redirect, url_for, current_app, jsonify, request

from Utilities.Authentication import Authentication
from Controllers import user_controller
from DAL.UserDAO import UserDAO


@user_controller.route('/')
def index():
    if 'auth_token' in session:
        try:
            user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
            login = UserDAO.get(user_id).login.split('@')[0]
            current_year = datetime.datetime.now().year.__str__()
            return render_template('userPanel.html', user=login, year=current_year)
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))


@user_controller.route('/logout')
def logout():
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index'))
