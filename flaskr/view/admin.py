from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.view.auth import admin_required, login_required
from flaskr.model import Bill, Restaurant, Order, User, Meal
from flaskr.tasks import send_bill_mail

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
            restaurant.unavailable_meals.sort(key=lambda x: x.average_stars if x.average_stars else 0, reverse=True)
        elif sort_by == 'price':
            meals.sort(key=lambda x: x.price)
            restaurant.unavailable_meals.sort(key=lambda x: x.price)
        elif sort_by == 'sales':
            meals.sort(key=lambda x: x.sales, reverse=True)
            restaurant.unavailable_meals.sort(key=lambda x: x.sales, reverse=True)
        return render_template("admin/edit_restaurant.html", restaurant=restaurant, meals=meals, sort_by=sort_by)
    elif request.method == 'POST':
        new_name = request.form['restaurant_name']
        new_tag = request.form['restaurant_tag']
        Restaurant.update(id, new_name, new_tag)

        return redirect(url_for('admin.edit_restaurant', id=id))

@bp.route('/hide_restaurant/<int:id>/', methods=['POST'])
@admin_required
def hide_restaurant(id):
    Restaurant.hide(id)
    restaurants = Restaurant.getAll()
    return render_template('admin/index.html', restaurants=restaurants, edit=None)

@bp.route('/add_restaurant/', methods=['GET','POST'])
@admin_required
def add_restaurant():
    restaurant_id = Restaurant.add()
    restaurant = Restaurant.getById(restaurant_id)
    return render_template("admin/edit_restaurant.html", restaurant=restaurant, meals=None, sort_by=None)

@bp.route('/edit_meal/<int:id>/', methods=['POST'])
@admin_required
def edit_meal(id):
    new_name = request.form['meal_name']
    new_price = request.form['meal_price']
    new_description = request.form['meal_description']
    rest_id = request.form['rest_id']
    Meal.update(id, new_name, new_description, new_price)

    return redirect(url_for('admin.edit_restaurant', id=rest_id))

@bp.route('/add_meal/<int:restaurant_id>/', methods=['POST'])
@admin_required
def add_meal(restaurant_id):
    new_name = request.form['meal_name']
    new_price = request.form['meal_price']
    new_description = request.form['meal_description']
    # rest_id = request.form['rest_id']
    Meal.add(restaurant_id, new_name, new_description, new_price)

    return redirect(url_for('admin.edit_restaurant', id=restaurant_id))

@bp.route('/hide_meal/<int:id>/', methods=['POST'])
@admin_required
def hide_meal(id):
    Meal.hide(id)
    rest_id = request.form['rest_id']

    return redirect(url_for('admin.edit_restaurant', id=rest_id))

@bp.route('/recover_meal/<int:id>/', methods=['POST'])
@admin_required
def recover_meal(id):
    Meal.recover(id)
    rest_id = request.form['rest_id']

    return redirect(url_for('admin.edit_restaurant', id=rest_id))

@bp.route("/bill", methods=["GET"])
@admin_required
def check_bill():
    bill_data = Bill.get_user_bills()
    return render_template('admin/bill.html', bill_data = bill_data)

@bp.route("/send_bill", methods=["POST"])
@admin_required
def send_bill():
    send_bill_mail.delay()

    flash("已將工作傳送至後台執行", "info")

    return redirect(url_for('admin.check_bill'))
