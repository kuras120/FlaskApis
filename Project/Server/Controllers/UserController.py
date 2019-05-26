import os
import ast
import json
import redis
import datetime
import urllib.parse

from flask import Blueprint

from rq import Queue, Connection

from werkzeug.utils import secure_filename

from Project.Server.DAL.UserDAO import UserDAO
from Project.Server.DAL.FileDAO import FileDAO

from Project.Server.Tasks.TestTask import run_algorithm

from Project.Server.Utilities.Authentication import Authentication

from flask import render_template, session, redirect, url_for, current_app, request, jsonify

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/')
@user_controller.route('/<text>')
def index(text=None):
    user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
    try:
        login = user.login.split('@')[0]
        files = FileDAO.get_all(user.id)
        current_year = datetime.datetime.now().year.__str__()

        if text:
            text = ast.literal_eval(text)
        return render_template('userPanel.html', user=login, home_catalog=user.home_catalog, files=files,
                               year=current_year, text=text)
    except Exception as e:
        return redirect(url_for('home_controller.logout', text=['warning', e]))


# TODO Ma zwracac jsona
@user_controller.route('/files', methods=['POST'])
def add_file():
    file = request.files['file-input']
    try:
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        FileDAO.create(file, user)
        return redirect(url_for('user_controller.index', text=['success', secure_filename(file.filename) + ' added.']))
    except Exception as e:
        return redirect(url_for('user_controller.index', text=['warning', e]))


@user_controller.route('/files/<string:name>', methods=['PUT'])
def change_file(name):
    try:
        data = json.loads(request.get_data().decode('utf-8'))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        file_to_update = FileDAO.read(name, user.id)
        file_to_update.name = data[0]
        FileDAO.update(file_to_update, user, 'File name: ' + name + ' to ' + data[0] + ' updated')
        return jsonify({'old': name, 'new': data[0]}), 202
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@user_controller.route('/files', methods=['DELETE'])
def delete_files():
    try:
        data = json.loads(urllib.parse.unquote(request.get_data('files').decode('utf-8')))
        user = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token']))
        data_entities = []
        for name in data:
            data_entities.append(FileDAO.read(name, user.id))
        FileDAO.delete(data_entities, user.home_catalog)
        return jsonify({'deleted': data}), 202
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@user_controller.route('/queue_task', methods=['POST'])
def queue_task():
    alg_path = ast.literal_eval(request.form['alg_path'])
    file_path = request.form['file_path']
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue(default_timeout=3600)
        task = q.enqueue(run_algorithm, alg_path[1], file_path)

    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id(),
            'task_name': alg_path[0],
            'file_name': os.path.basename(file_path)
        }
    }
    return jsonify(response_object), 202


@user_controller.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)


@user_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', text=['warning', e]))
    else:
        return redirect(url_for('home_controller.index', text=['warning', 'You have to log in first.']))
