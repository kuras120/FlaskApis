import logging

from flask import Flask

from Controllers.HomeController import home_controller

app = Flask(__name__)
app.register_blueprint(home_controller, url_prefix='/')

main_logger = logging.getLogger('logger')
main_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

main_logger.addHandler(fh)
main_logger.addHandler(ch)

main_logger.info("Server started.")

# TODO logger tylko do najwazniejszych operacji. Zamiast niego historia do bazy danych.
