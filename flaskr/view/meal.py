import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Meal, Review

bp = Blueprint('meal', __name__, url_prefix='/meal')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def index(id):
    meal = Meal.getById(id)
    return render_template("meal/index.html", meal=meal, reviews = meal.reviews)

@bp.route('/writeReview/<int:id>/', methods=('GET', 'POST'))
def writeReview(id):
    if request.method == 'POST':
        user_id = g.user.id
        meal_id = id
        stars = request.form["rating"]
        content = request.form["content"]
        error = None

        if error is None:
            Review.newReview(user_id, meal_id, stars, content)
        else:
            flash(error)

        return redirect( url_for('meal.index', id=id) )
    elif request.method == 'GET':
        if Review.get_comment_by_meal_id_and_user_id(id, g.user.id):
            
            return redirect( url_for('home.orders') )
        else:
            meal = Meal.getById(id)
            return render_template("meal/writeReview.html", meal=meal)
    # meal = Meal.getById(id)
    # return render_template("meal/writeReview.html", meal=meal)
