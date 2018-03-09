from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index/<user>')
def hello_world(user):
    return render_template('index.html', name=user)


if __name__ == '__main__':
    app.run(debug=True)


