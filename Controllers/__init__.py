import logging

from flask import Flask

from ORM.DbConfig import init_db, db_session

from Controllers.HomeController import home_controller

main_logger = logging.getLogger('logger')
error_logger = logging.getLogger('error_logger')

main_logger.setLevel(logging.DEBUG)
error_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('info.log')
fh.setLevel(logging.DEBUG)

fher = logging.FileHandler('error.log')
fher.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

fher.setFormatter(formatter)
ch.setFormatter(formatter)

main_logger.addHandler(fh)

error_logger.addHandler(fher)
error_logger.addHandler(ch)

app = Flask(__name__)
app.register_blueprint(home_controller, url_prefix='/')
main_logger.info("Blueprints created.")
init_db()
main_logger.info("Server started.")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# TODO logger tylko do najwazniejszych operacji. Zamiast niego historia do bazy danych.
