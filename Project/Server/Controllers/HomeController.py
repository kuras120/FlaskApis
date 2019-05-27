import ast
import datetime

from flask import Blueprint

from multiprocessing import Value

from Project.Server.DAL.UserDAO import UserDAO

from Project.Server.Utilities.Format import Format
from Project.Server.Utilities.Authentication import Authentication
from Project.Server.Utilities.PropertiesReader import PropertiesReader

from flask import render_template, jsonify, request, session, redirect, url_for, current_app

home_controller = Blueprint('home_controller', __name__)

survey = PropertiesReader('Project/Client/static/dictionary/feedback_index.properties')
likes_counter = Value('i', 1200)


@home_controller.route('/')
@home_controller.route('/<text>/')
def index(text=None):
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    likes = Format.human_format(likes_counter.value)
    current_year = datetime.datetime.now().year.__str__()
    question_data = survey.read('key1')
    login = None
    if 'auth_token' in session:
        try:
            login = UserDAO.get(Authentication.decode_auth_token(current_app.config['SECRET_KEY'],
                                                                 session['auth_token'])).login.split('@')[0]
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', text=['warning', e.__str__()]))

    if text:
        text = ast.literal_eval(text)
    return render_template('index.html', date=current_date, year=current_year, user=login, likes=likes,
                           question_data=question_data, text=text)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    with likes_counter.get_lock():
        likes_counter.value += 1
    number = Format.human_format(likes_counter.value)
    return jsonify(number)


@home_controller.route('/login_process', methods=['POST'])
def login_process():
    try:
        user = UserDAO.read(request.form['email'], request.form['password'])
        session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('home_controller.index', text=['warning', e]))


@home_controller.route('/register_process', methods=['POST'])
def register_process():
    if request.form['password'] == request.form['conf_password']:
        try:
            user = UserDAO.create(request.form['email'], request.form['password'])
            session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
            return redirect(url_for('user_controller.index'))
        except Exception as e:
            return redirect(url_for('home_controller.index', text=['warning', e]))
    else:
        return redirect(url_for('home_controller.index', text=['warning', 'Passwords don\'t match.']))


@home_controller.route('/logout')
@home_controller.route('/logout/<text>')
def logout(text=None):
    session.pop('auth_token', None)
    return redirect(url_for('home_controller.index', text=text))
