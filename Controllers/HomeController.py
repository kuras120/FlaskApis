import logging
import datetime
import traceback

from flask import Blueprint
from flask import render_template, jsonify, request

from ORM.DbConfig import DbConfig

from BLL.UserManager import UserManager

from Utilities.Counter import Counter
from Utilities.NumberFormat import NumberFormat
from Utilities.PropertiesReader import PropertiesReader

logger = logging.getLogger('logger')
home_controller = Blueprint('home_controller', __name__)
data = PropertiesReader('Controllers/static/dictionary/feedback_index.properties')

db = DbConfig()
likes_counter = Counter(990)


@home_controller.route('/')
def index():
    current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
    number = NumberFormat.human_format(likes_counter.get_likes())
    complete_data = data.read('key1')
    current_year = datetime.datetime.now().year.__str__()
    return render_template('index.html', date=current_date, likes=number, question_data=complete_data,
                           year=current_year)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
    likes_counter.add_like()
    logger.info('Like added.')
    number = NumberFormat.human_format(likes_counter.get_likes())
    return jsonify(number)


@home_controller.route('/user/panel', methods=['POST'])
def login_process():
    try:
        manager = UserManager(db.get_session())
        login = request.form['email']
        password = request.form['password']
        user = manager.check_user(login, password)
        logger.info("User " + user.login + " signed in.")
        return render_template('userPanel.html', user=user.login)

    except Exception as e:
        tb = traceback.format_exc(limit=-1)
        logger.error(e.__str__() + "\n" + tb.__str__())
        return render_template('error.html', error='Incorrect login data.')

# TODO Partial view (widget)
