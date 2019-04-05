import datetime

from flask import render_template, jsonify, request, session, redirect, url_for, current_app

from Utilities.PropertiesReader import PropertiesReader
from Utilities.Authentication import Authentication
from Controllers import home_controller
from DAL.UserManager import UserManager
from Utilities.Counter import Counter
from Utilities.Format import Format


survey = PropertiesReader('static/dictionary/feedback_index.properties')
# TODO Refactor required https://stackoverflow.com/a/23417696
likes_counter = Counter(990)


@home_controller.route('/', defaults={'error': None})
@home_controller.route('/<error>')
def index(error):
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    likes = Format.human_format(likes_counter.get())
    current_year = datetime.datetime.now().year.__str__()
    question_data = survey.read('key1')
    login = None
    if 'auth_token' in session:
        error = None
        try:
            user_id = Authentication.decode_auth_token(current_app.config['SECRET_KEY'], session['auth_token'])
            login = UserManager.get_user(user_id).login.split('@')[0]
        except Exception as e:
            session.pop('auth_token', None)
            return redirect(url_for('home_controller.index', error=e))

    return render_template('index.html', date=current_date, year=current_year, user=login, likes=likes,
                           question_data=question_data, error=error)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    likes_counter.add(1)
    number = Format.human_format(likes_counter.get())
    return jsonify(number)


@home_controller.route('/login_process', methods=['POST'])
def login_process():
    try:
        user = UserManager.read_user(request.form['email'], request.form['password'])
        session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
        return redirect(url_for('user_controller.index'))
    except Exception as e:
        return redirect(url_for('home_controller.index', error=e))


@home_controller.route('/register_process', methods=['POST'])
def register_process():
    if request.form['password'] == request.form['conf_password']:
        try:
            user = UserManager.create_user(request.form['email'], request.form['password'])
            session['auth_token'] = Authentication.encode_auth_token(current_app.config['SECRET_KEY'], user.id)
            return redirect(url_for('user_controller.index'))
        except Exception as e:
            return redirect(url_for('home_controller.index', error=e))
    else:
        return redirect(url_for('home_controller.index', error='Passwords don\'t match.'))
