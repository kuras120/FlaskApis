from Utilities.PropertiesReader import PropertiesReader
from flask import render_template, jsonify, request
from Utilities.NumberFormat import NumberFormat
from Utilities.Counter import Counter
from flask import Blueprint
import datetime
import logging

data = PropertiesReader('Controllers/static/dictionary/feedback_index.properties')
home_controller = Blueprint('home_controller', __name__)
logger = logging.getLogger('base_logger')
likes_counter = Counter(990)


@home_controller.route('/')
def index():
	current_date = datetime.datetime.now().date().strftime('%B %d, %Y')
	number = NumberFormat.human_format(likes_counter.get_likes())
	complete_data = data.read('key1')
	current_year = datetime.datetime.now().year.__str__()
	return render_template('index.html', date=current_date, likes=number, question_data=complete_data, year=current_year)


@home_controller.route('/add_like', methods=['POST'])
def add_like():
	likes_counter.add_like()
	logger.info('Like added.')
	number = NumberFormat.human_format(likes_counter.get_likes())
	return jsonify(number)


# TODO: create login
@home_controller.route('/login_process', methods=['POST'])
def login_process():
	login = request.form['email']
	password = request.form['password']
	return jsonify({'login': login, 'password': password})
