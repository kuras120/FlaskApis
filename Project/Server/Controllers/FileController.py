import json

from flask import Blueprint

from Project.Server.DAL.UserDAO import UserDAO
from Project.Server.DAL.FileDAO import FileDAO

from flask import session, current_app, request, jsonify, url_for

from Project.Server.Utilities.Authentication import Authentication

file_controller = Blueprint('file_controller', __name__)


@file_controller.route('/files/<string:name>', methods=['GET'])
def get_file(name):
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        file = FileDAO.read(name, user.id)
        return jsonify({'name': file.name, 'added_on': file.added_on.__str__()}), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@file_controller.route('/files', methods=['GET'])
def get_files():
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        files = FileDAO.get_all(user.id)
        file_list = []
        for file in files:
            file_list.append({'name': file.name, 'added_on': file.added_on.__str__()})

        return jsonify({'files': file_list}), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@file_controller.route('/files', methods=['POST'])
def add_file():
    file = request.files['file']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        new_file = FileDAO.create(file, user)
        return jsonify({'name': new_file.name, 'added_on': new_file.added_on.__str__()}), 201
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@file_controller.route('/files/<string:name>', methods=['PUT'])
def change_file(name):
    try:
        data = json.loads(request.get_data().decode('utf-8'))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        file_to_update = FileDAO.read(name, user.id)
        file_to_update.name = data[0]
        FileDAO.update(file_to_update, user, 'File name: ' + name + ' to ' + data[0] + ' updated')
        return jsonify({'old_name': name, 'new_name': data[0]}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500


@file_controller.route('/files', methods=['DELETE'])
def delete_files():
    try:
        data = json.loads(request.get_data().decode('utf-8'))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        data_entities = []
        for name in data:
            data_entities.append(FileDAO.read(name, user.id))
        FileDAO.delete(data_entities, user.home_catalog)
        return jsonify({'deleted_files': data}), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@file_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return jsonify({'redirect': url_for('home_controller.logout', text=['warning', e.__str__()])}), 401
    else:
        return jsonify({'redirect': url_for('home_controller.index',
                                            text=['warning', 'You have to log in first.'])}), 401
