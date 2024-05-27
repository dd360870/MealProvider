import os
from os import environ

from flask import Flask, current_app
from flaskr.commands import register_cli

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

    DEBUG = environ.get('DEBUG')
    DB_HOST = environ.get('DB_HOST')

    app.config["DEBUG"] = (DEBUG == '1')
    app.config["DB_HOST"] = DB_HOST
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mariadb+mariadbconnector://nol:nol@{DB_HOST}:3306/meal_provider"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            'connect_timeout': 10
        }
    }

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

    from flaskr.view import auth, home, restaurant, admin, clerk
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(restaurant.bp)
    app.register_blueprint(clerk.bp)
    app.add_url_rule('/', endpoint='index')

    return app
