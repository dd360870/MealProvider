import os

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

    # a simple page that says hello
    @app.route('/ping')
    def ping():
        return 'pong'

    from .db import db

    app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://nol:nol@db:3306/meal_provider"
    # initialize the app with the extension
    db.init_app(app)
    # init table
    with app.app_context():
        db.create_all()

        register_cli(app)

    from .view import auth, home, restaurant, admin, clerk
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(restaurant.bp)
    app.register_blueprint(clerk.bp)
    app.add_url_rule('/', endpoint='index')

    return app
