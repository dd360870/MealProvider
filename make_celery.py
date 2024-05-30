from flaskr import create_app

from flaskr.tasks import *

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
