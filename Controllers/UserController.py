import datetime

from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO
from Controllers import user_controller
from Utilities.Authentication import Authentication

from flask import render_template, session, redirect, url_for, current_app


@user_controller.route('/', defaults={'error': None})
@user_controller.route('/<error>')
def index(error):
    user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
    try:
        login = user.login.split('@')[0]
        files = FileDAO.get_all(user.id)
        current_year = datetime.datetime.now().year.__str__()
        return render_template('userPanel.html', user=login, files=files, year=current_year, error=error)
    except Exception as e:
        return redirect(url_for('home_controller.logout', error=e))


@user_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))
