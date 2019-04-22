from DAL.UserDAO import UserDAO
from DAL.DataDAO import DataDAO
from Controllers import operation_controller
from Utilities.Authentication import Authentication

from flask import session, redirect, url_for, current_app, request


@operation_controller.route('/add_file', methods=['POST'])
def add_file():
    file = request.files['file-input']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        DataDAO.create(file, user)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


@operation_controller.route('/add_file', methods=['POST'])
def delete_files():
    raise NotImplementedError


@operation_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))
