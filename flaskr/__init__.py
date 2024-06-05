import os
from os import environ

from flask import Flask, current_app
from flaskr.commands import register_cli

from celery import Celery, Task
from celery.schedules import crontab
from flask_mail import Mail, Message

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    "disable_existing_loggers": False,
})

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    DB_HOST = environ.get('DB_HOST')
    REDIS_HOST = environ.get('REDIS_HOST')
    MAILGUN_USERNAME = environ.get('MAILGUN_USERNAME')
    MAILGUN_PASSWORD = environ.get('MAILGUN_PASSWORD')

    app.config["DB_HOST"] = DB_HOST
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mariadb+mariadbconnector://nol:nol@{DB_HOST}:3306/meal_provider"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            'connect_timeout': 10
        }
    }

    # Initialize Celery
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"redis://{REDIS_HOST}",
            result_backend=f"redis://{REDIS_HOST}",
            task_ignore_result=True,
            broker_connection_retry_on_startup=True,
            beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'flaskr.tasks.save_bill',
                    'schedule': crontab(hour=7, minute=30, day_of_month=1),
                    'args': (),
                },
            },
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    # Initialize SMTP
    app.config['MAIL_SERVER'] = 'smtp.mailgun.org'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = MAILGUN_USERNAME
    app.config['MAIL_PASSWORD'] = MAILGUN_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = 'admin@mealprovider.nollab.me'

    mail = Mail(app)
    app.extensions["mail"] = mail

    # a simple page that says hello
    @app.route('/ping')
    def ping():
        return 'pong'

    from flaskr.db import db

    # initialize the app with the extension
    db.init_app(app)
    # init table
    with app.app_context():
        #db.create_all()

        register_cli(app)

    from flaskr.view import auth, home, restaurant, admin, clerk, meal
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(restaurant.bp)
    app.register_blueprint(clerk.bp)
    app.register_blueprint(meal.bp)
    app.add_url_rule('/', endpoint='index')

    return app
