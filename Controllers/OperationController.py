import json
import urllib.parse

from DAL.UserDAO import UserDAO
from DAL.FileDAO import FileDAO
from Controllers import operation_controller
from Utilities.Authentication import Authentication

from flask import session, redirect, url_for, current_app, request


@operation_controller.route('/add_file', methods=['POST'])
def add_file():
    file = request.files['file-input']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        FileDAO.create(file, user)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


@operation_controller.route('/delete_files', methods=['POST'])
def delete_files():
    try:
        data = json.loads(urllib.parse.unquote(request.get_data('files').decode('utf-8')))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        data_entities = []
        for name in data:
            data_entities.append(FileDAO.read(name, user.id))
        FileDAO.delete(data_entities, user.home_catalog)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('user_controller.index', error=e))


# TODO passing arguemnts to requests
@operation_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', error=e))
    else:
        return redirect(url_for('home_controller.index', error='You have to log in first.'))
