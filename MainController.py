from flask import Flask
from HomeController import *

app = Flask(__name__)
app.register_blueprint(home_controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
