from flask import render_template, jsonify
from flask import Blueprint
import datetime

from Utilities.Counter import Counter
from Utilities.NumberFormat import NumberFormat
from Utilities.PropertiesReader import PropertiesReader, Method

home_controller = Blueprint('home_controller', __name__)

likes_counter = Counter(990)
data = PropertiesReader("Controllers/static/dictionary/feedback_index.properties")


@home_controller.route('/')
def index():
    current_date = datetime.datetime.now().date().strftime("%B %d, %Y")
    number = NumberFormat.human_format(likes_counter.get_likes())
    complete_data = data.read("key1", Method.Manual_properties)
    current_year = datetime.datetime.now().year.__str__()
    return render_template('index.html', date=current_date, likes=number, question_data=complete_data, year=current_year)


@home_controller.route('/add_like/')
def add_like():
    likes_counter.add_like()
    number = NumberFormat.human_format(likes_counter.get_likes())
    print("Like added")
    return jsonify(number)

#TODO create login route