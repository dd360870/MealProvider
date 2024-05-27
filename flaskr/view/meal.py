import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Meal

bp = Blueprint('meal', __name__, url_prefix='/meal')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def index(id):
    meal = Meal.getById(id)
    return render_template("meal/index.html", meal=meal, reviews = meal.reviews)

@bp.route('/writeReview/<int:id>/', methods=('GET', 'POST'))
def writeReview(id):
    if request.method == 'POST':
        start
    meal = Meal.getById(id)
    return render_template("meal/writeReview.html", meal=meal)