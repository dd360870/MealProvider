from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.view.auth import admin_required, login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/")
@admin_required
def index():
    return render_template('admin/index.html')

from flaskr.model import Order, User
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
    #print(user_id_to_name)
    #print(user_bill_data)
    return render_template('admin/bill.html', user_bill_data = user_bill_data, user_id_to_name=user_id_to_name)