from flask import Flask, render_template, jsonify
import datetime

from Utilities.Counter import Counter
from Utilities.NumberFormat import NumberFormat

app = Flask(__name__)


@app.route('/')
def index():
    current_date = datetime.datetime.now().date().strftime("%B %d, %Y")
    number = NumberFormat.human_format(Counter.get_instance().get_likes())
    return render_template('index.html', date=current_date, likes=number)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/add_like/')
def add_like():
    instance = Counter.get_instance()
    instance.add_like()
    number = NumberFormat.human_format(instance.get_likes())
    print("Like added")
    return jsonify(number)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
