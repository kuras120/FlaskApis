import os
import redis
import logging

from flask.cli import FlaskGroup
from rq import Connection, Worker

from Project.Server import create_app
from Project.Server.Config import init_loggers, init_debug, init_db


app = create_app()
cli = FlaskGroup(create_app=create_app)

init_loggers()
logging.getLogger('logger').info('Loggers initialized.')

init_db(app)
logging.getLogger('logger').info('Db initialized.')

if os.getenv('FLASK_ENV') == 'development':
    init_debug()
    logging.getLogger('logger').info('Debug mode on')


@cli.command('run_worker')
def run_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()


if __name__ == '__main__':
    cli()
