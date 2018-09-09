from flask import Flask, render_template

application = Flask(__name__)


@application.route('/')
def start():
    return render_template('index.html')


@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
