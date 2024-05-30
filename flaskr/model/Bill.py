from sqlalchemy import func, extract, desc
from datetime import datetime, timedelta, date
from flaskr.db import db, Order, Bill
import calendar
import logging

def get_user_bills():
    bills_all = Bill.query.where(Bill.is_paid==False).order_by(desc(Bill.bill_month)).all()

    users = list(set([b.user for b in bills_all]))
    users.sort(key=lambda u:u.username)

    bill_data = {}

    for u in users:
        bill_data[u.id] = {
            'user': u,
            'detail': [],
        }

    for row in bills_all:
        bill_data[row.user_id]['detail'].append({
            "username": row.user.username,
            "date": row.bill_month,
            "amount": row.amount,
            "is_paid": row.is_paid,
            "paid_datetime": row.paid_datetime
        })
    
    return bill_data.values()

def get_bills(year, month):
    return Bill.query.where(Bill.bill_month==date(year, month, 1)).all()

def save_bills(year=None, month=None):

    if year is None or month is None:
        # fetch last month of today
        last_month = date.today().replace(day=1) - timedelta(days=1)
        arg_year = last_month.year
        arg_month = last_month.month

    _, last = calendar.monthrange(arg_year, arg_month)
    month_begin = datetime(arg_year, arg_month, 1, 0, 0, 0)
    month_end = datetime(arg_year, arg_month, last, 23, 59, 59)

    logging.info(f"Calculating Bills from {month_begin} to {month_end}")

    orders = Order.query.with_entities(
            Order.user_id,
            func.sum(Order.total_price).label('total_price'),
            extract('year', Order.timestamp).label('year'),
            extract('month', Order.timestamp).label('month')
        )\
        .where(Order.timestamp.between(month_begin, month_end))\
        .group_by(Order.user_id, extract('year', Order.timestamp), extract('month', Order.timestamp))\
        .order_by(desc('year'), desc('month'))\
        .all()

    for o in orders:
        bill = Bill(
            user_id=o.user_id,
            bill_month=date(o.year, o.month, 1),
            amount=o.total_price,
        )
        db.session.add(bill)
    db.session.commit()