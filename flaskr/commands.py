import os
from flask import Flask, current_app
from flask.cli import AppGroup
from werkzeug.security import check_password_hash, generate_password_hash

def register_cli(app: Flask):
    db_cli = AppGroup('db', short_help='Database utilities')

    from flaskr.db import db

    @db_cli.command('init', short_help='Initialize Database')
    def init():
        db.drop_all()
        db.create_all()

    @db_cli.command('add_mock', short_help="Add mock data to database")
    def add_mock():
        db_host = current_app.config["DB_HOST"]
        os.system(f"mariadb -h {db_host} -u nol -pnol meal_provider < data.sql")
        from flaskr.mock import add_orders

        add_orders()

    @db_cli.command('cli', short_help='Connect to Database CLI')
    def cli():
        db_host = current_app.config["DB_HOST"]
        os.system(f"mariadb -h {db_host} -u nol -pnol meal_provider")

    app.cli.add_command(db_cli)
