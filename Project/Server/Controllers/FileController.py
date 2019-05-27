import json
import urllib.parse

from flask import Blueprint

from Project.Server.DAL.UserDAO import UserDAO
from Project.Server.DAL.FileDAO import FileDAO

from Project.Server.Utilities.Authentication import Authentication

from flask import session, current_app, request, jsonify

file_controller = Blueprint('file_controller', __name__)


@file_controller.route('/files/<string:name>', methods=['GET'])
def get_file(name):
    pass


@file_controller.route('/files', methods=['GET'])
def get_files():
    pass


@file_controller.route('/files', methods=['POST'])
def add_file():
    file = request.files['file']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        new_file = FileDAO.create(file, user)
        return jsonify({'name': new_file.name, 'date': new_file.added_on.__str__()}), 201
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
        return jsonify({'old': name, 'new': data[0]}), 200
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
        return jsonify({'deleted': data}), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500