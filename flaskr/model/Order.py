from sqlalchemy import func, desc, extract, select
from flaskr.db import db, Order, OrderItem
from datetime import datetime, timedelta
import calendar

def getGroupByMonth(user_id):
    """Get count, year, month group by month in recent 1 year range
    """

    today = datetime.now()
    bdate = datetime(today.year-1, today.month, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

    return Order.query.with_entities(
                func.count().label('count'),
                extract('year', Order.timestamp).label('year'),
                extract('month', Order.timestamp).label('month')
            )\
            .where(Order.user_id == user_id)\
            .where(Order.timestamp >= bdate)\
            .group_by(extract('year', Order.timestamp), extract('month', Order.timestamp))\
            .order_by(desc('year'), desc('month'))\
            .all()

def getHistory(user_id, year, month):
    """Get order history by year and month
    """

    _, last = calendar.monthrange(year, month)

    bdate = datetime(year, month, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    edate = datetime(year, month, last, 23, 59, 59).strftime("%Y-%m-%d %H:%M:%S")

    return Order.query\
        .where(Order.user_id == user_id)\
        .where(Order.timestamp.between(bdate, edate))\
        .order_by(desc(Order.timestamp))\
        .all()
