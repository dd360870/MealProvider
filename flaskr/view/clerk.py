from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Restaurant, Meal, User
from flaskr.view.auth import clerk_required

bp = Blueprint('clerk', __name__, url_prefix='/clerk')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
@clerk_required
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
    return render_template("clerk/index.html", restaurant=restaurant, meals=meals, sort_by=sort_by)

from flaskr.model.User import validate_customer_id
@bp.route('/register_customer/', methods=('GET', 'POST'))
@clerk_required
def register_customer():
    customer_data = None
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        customer_data = validate_customer_id(customer_id)
        session['customer_id'] = customer_data.id
    return render_template('clerk/register_customer.html', customer_data=customer_data)

@bp.route('/process_qr/', methods=('GET', 'POST'))
@clerk_required
def process_qr():
    customer_data = None
    qr_result = request.form['qrResult']
    if qr_result:
        customer_data = validate_customer_id(int(qr_result))
        session['customer_id'] = customer_data.id
    return render_template('clerk/register_customer.html', customer_data=customer_data)

from flaskr.model import Order, Meal
@bp.route('/new_order/', methods=('GET', 'POST'))
@clerk_required
def new_order():
    id = g.user.restaurant_id
    restaurant = Restaurant.getById(id)
    return render_template('clerk/new_order.html', restaurant=restaurant, meals=restaurant.meals)

@bp.route('/confirm_order/', methods=('GET', 'POST'))
@clerk_required
def confirm_order():
    restaurant_id = g.user.restaurant_id
    restaurant = Restaurant.getById(restaurant_id)
    total_price = 0
    order_details = []
    for key in request.form.keys():
        if key.startswith('quantity_'):
            meal_id = int(key.split('_')[1])
            quantity = int(request.form.get(key))
            if quantity > 0:
                price = Meal.get_price_by_id(meal_id)
                total_price = total_price + price
                order_details.append({
                    'meal_id': meal_id,
                    'count': quantity,
                    'price': price
                })
    if total_price == 0:
        return render_template('clerk/new_order.html', restaurant=restaurant, meals=restaurant.meals)
    else:
        order = Order.add_order(user_id = session.get('customer_id'), total_price=total_price, restaurant_id=restaurant_id)
        Order.create_order_items(order.id, order_details)
        return render_template('clerk/finish_order.html', customer=validate_customer_id(session.get('customer_id')), total_price = total_price, order_item = order.items)
    
@bp.route('/cancel_orders/', methods=('GET', 'POST'))
@clerk_required
def show_order():
    user_id_to_name = {}
    users = User.getAll()
    for user in users:
        user_id_to_name[user.id] = user.username
    # ord =Order.getAll()
    # for i in ord.items:
    #     print(i)
    return render_template('clerk/cancel_order.html', orders=Order.get_restaurant_order(g.user.restaurant_id), user_id_to_name=user_id_to_name)
@bp.route('/redirect_to_cancel_orders/', methods=('GET', 'POST'))
@clerk_required
def cancel_orders():
    cancelled_orders = request.form.getlist('cancel_orders[]')
    print(cancelled_orders)
    Order.delete_orders(cancelled_orders)
    return redirect(url_for('clerk.show_order'))

@clerk_required
@bp.route('/review<int:id>/', methods=('GET', 'POST'))
def review(id):
    meal = Meal.getById(id)
    return render_template("clerk/review.html", meal=meal, reviews = meal.reviews)