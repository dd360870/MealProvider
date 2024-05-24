import click
from flask import Flask
from flask.cli import AppGroup
from werkzeug.security import check_password_hash, generate_password_hash

def register_cli(app: Flask):
    db_cli = AppGroup('db', short_help='Database utilities')

    from flaskr.db import db
    import flaskr.db as orm

    @db_cli.command('init', short_help='Initialize Database')
    def init():
        db.drop_all()
        db.create_all()

    app.cli.add_command(db_cli)
