from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.model import Restaurant

bp = Blueprint('clerk', __name__, url_prefix='/clerk')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def index(id):
    restaurant = Restaurant.getById(id)
    return render_template('clerk/index.html', restaurant=restaurant, meals=restaurant.meals)

from flaskr.model.User import validate_customer_id
@bp.route('/register_customer/', methods=('GET', 'POST'))
def register_customer():
    customer_data = None
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        customer_data = validate_customer_id(customer_id)
        session['customer_id'] = customer_data.id
    return render_template('clerk/register_customer.html', customer_data=customer_data)

from flaskr.model import Order, Meal
@bp.route('/new_order/', methods=('GET', 'POST'))
def new_order():
    id = g.user.restaurant_id
    restaurant = Restaurant.getById(id)
    return render_template('clerk/new_order.html', restaurant=restaurant, meals=restaurant.meals)

@bp.route('/confirm_order/', methods=('GET', 'POST'))
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
                price = price*quantity
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
