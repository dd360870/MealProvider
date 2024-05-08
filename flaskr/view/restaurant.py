import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Restaurant

bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def index(id):
    restaurant = Restaurant.getById(id)
    return render_template("restaurant/index.html", restaurant=restaurant, meals=restaurant.meals)