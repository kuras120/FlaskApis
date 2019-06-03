import os
import ast
import redis
import datetime

from flask import Blueprint

from rq import Queue, Connection

from Project.Server.DAL.UserDAO import UserDAO
from Project.Server.DAL.FileDAO import FileDAO

from Project.Server.Tasks.TestTask import run_algorithm, create_task

from rq.registry import StartedJobRegistry, FinishedJobRegistry

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
        return redirect(url_for('home_controller.logout', text=['warning', e.__str__()]))


@user_controller.route('/queue_task', methods=['POST'])
def queue_task():
    alg_path = ast.literal_eval(request.form['alg_path'])
    file_path = request.form['file_path']
    try:
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            q = Queue(default_timeout=3600)
            task = q.enqueue(run_algorithm, alg_path[1], file_path, result_ttl=86400)

            task.meta['task_name'] = alg_path[0]
            task.meta['file_name'] = os.path.basename(file_path)
            task.meta['token'] = Authentication.decode_auth_token(current_app.config['SECRET_KEY'],
                                                                  session['auth_token'])
            task.save_meta()

        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_name': alg_path[0],
                'file_name': os.path.basename(file_path)
            }
        }
        return jsonify(response_object), 202
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@user_controller.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    try:
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
        return jsonify(response_object), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@user_controller.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            q = Queue()
            started = StartedJobRegistry().get_job_ids()
            finished = FinishedJobRegistry().get_job_ids()
            jobs = started + q.get_job_ids() + finished

            objects = []
            for element in jobs:
                task = q.fetch_job(element)
                if task.meta['token'] == Authentication.decode_auth_token(current_app.config['SECRET_KEY'],
                                                                          session['auth_token']):
                    if task:
                        response_object = {
                            'status': 'success',
                            'data': {
                                'task_id': task.get_id(),
                                'task_status': task.get_status(),
                                'task_result': task.result,
                                'task_name': task.meta['task_name'],
                                'file_name': task.meta['file_name']
                            }
                        }
                    else:
                        response_object = {'status': 'error'}
                    objects.append(response_object)
        return jsonify(objects), 200
    except Exception as e:
        return jsonify({'error': e.__str__()}), 500


@user_controller.before_request
def before_request():
    if 'auth_token' in session:
        try:
            Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
        except Exception as e:
            return redirect(url_for('home_controller.logout', text=['warning', e.__str__()]))
    else:
        return redirect(url_for('home_controller.index', text=['warning', 'You have to log in first.']))

