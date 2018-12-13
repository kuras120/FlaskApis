from flask import Flask
from Controllers.HomeController import *
import logging

app = Flask(__name__)
app.register_blueprint(home_controller)

logger = logging.getLogger('base_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('BaseLogs.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
