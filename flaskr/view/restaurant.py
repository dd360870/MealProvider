import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Restaurant

bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def index(id):
    sort_by = request.args.get('sort_by', None)
    restaurant = Restaurant.getById(id)
    meals = restaurant.meals
    if sort_by == 'stars':
        meals.sort(key=lambda x: x.average_stars if x.average_stars else 0, reverse=True)
    elif sort_by == 'price':
        meals.sort(key=lambda x: x.price)
    elif sort_by == 'sales':
        meals.sort(key=lambda x: x.sales, reverse=True)
    return render_template("restaurant/index.html", restaurant=restaurant, meals=meals, sort_by=sort_by)