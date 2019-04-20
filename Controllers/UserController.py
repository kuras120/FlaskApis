import datetime

from DAL.UserDAO import UserDAO
from DAL.DataDAO import DataDAO
from Controllers import user_controller
from Utilities.Authentication import Authentication

from flask import render_template, session, redirect, url_for, current_app, jsonify, request


@user_controller.route('/account', defaults={'error': None})
@user_controller.route('/account/<error>')
def index(error):
    if 'auth_token' in session:
        try:
            user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'],
                                                                session['auth_token']))
            login = user.login.split('@')[0]
            files = DataDAO.get_all(user.id)
            current_year = datetime.datetime.now().year.__str__()
            return render_template('userPanel.html', user=login, files=files, year=current_year, error=error)
        except Exception as e:
            return redirect(url_for('user_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))


@user_controller.route('/add_file', methods=['POST'])
def add_file():
    file = request.files['fileInput']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        DataDAO.create(file, user)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


@user_controller.route('/logout', defaults={'error': None})
@user_controller.route('/logout/<error>')
def logout(error):
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index', error=error))
