from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.view.auth import admin_required, login_required
from flaskr.model import Restaurant, Order, User, Meal
from flaskr.db import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_required
def index():
    selected_tags = request.args.getlist('tag')
    restaurants = Restaurant.getByTags(selected_tags)
    return render_template('admin/index.html', restaurants=restaurants, edit=None)

@bp.route('/edit_restaurant/<int:id>/', methods=('GET', 'POST'))
@admin_required
def edit_restaurant(id):
    if request.method == 'GET':
        sort_by = request.args.get('sort_by', None)
        restaurant = Restaurant.getById(id)
        meals = restaurant.meals
        if sort_by == 'stars':
            meals.sort(key=lambda x: x.average_stars if x.average_stars else 0, reverse=True)
        elif sort_by == 'price':
            meals.sort(key=lambda x: x.price)
        elif sort_by == 'sales':
            meals.sort(key=lambda x: x.sales, reverse=True)
        return render_template("admin/edit_restaurant.html", restaurant=restaurant, meals=meals, sort_by=sort_by)
    elif request.method == 'POST':
        new_name = request.form['restaurant_name']
        new_tag = request.form['restaurant_tag']
        Restaurant.update(id, new_name, new_tag)

        return redirect(url_for('admin.edit_restaurant', id=id))

@bp.route('/edit_meal/<int:id>/', methods=['POST'])
@admin_required
def edit_meal(id):
    new_name = request.form['meal_name']
    new_price = request.form['meal_price']
    new_description = request.form['meal_description']
    rest_id = request.form['rest_id']
    Meal.update(id, new_name, new_description, new_price)

    return redirect(url_for('admin.edit_restaurant', id=rest_id))


@bp.route("/bill", methods=('GET', 'POST'))
@admin_required
def check_bill():
    bill_data = Order.get_bill()
    user_id_to_name = {}
    users = User.getAll()
    for user in users:
        user_id_to_name[user.id] = user.username
    user_bill_data = {}
    for item in bill_data:
        user_id, price, year, month = item
        if user_id not in user_bill_data:
            user_bill_data[user_id] = []
        user_bill_data[user_id].append((int(price), year, month))
    print(user_id_to_name)
    print(user_bill_data)
    return render_template('admin/bill.html', user_bill_data = user_bill_data, user_id_to_name=user_id_to_name)
