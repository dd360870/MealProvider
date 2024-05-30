from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.view.auth import admin_required, login_required
from flaskr.model import Bill
from flaskr.tasks import send_bill_mail

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/")
@admin_required
def index():
    return render_template('admin/index.html')

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
