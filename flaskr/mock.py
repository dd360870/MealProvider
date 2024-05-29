import random
from datetime import datetime, timedelta, date
from flaskr.db import db, User, Restaurant, Order, Bill, Meal, OrderItem
from sqlalchemy import func, extract
import calendar

def random_datetime():
    # 範圍：兩年前到今天
    sdate = datetime.now()-timedelta(days=365*2)
    random_ts = random.randint(round(sdate.timestamp()), round(datetime.now().timestamp()))
    random_dt = datetime.fromtimestamp(random_ts).strftime("%Y-%m-%d %H:%M:%S")
    return random_dt

def add_orders():

    users = User.query.all()
    restaurants = Restaurant.query.all()

    if len(users) == 0:
        raise Exception("Please insert \"User\" table first.")

    for _ in range(100*len(users)):
        restaurant = random.choice(restaurants)
        order = Order(total_price=0, timestamp=random_datetime(), user_id=random.choice(users).id, restaurant_id=restaurant.id)

        # make sure order has id
        db.session.add(order)
        db.session.flush()

        meals = Meal.query.where(Meal.restaurant_id==restaurant.id).all()

        # 餐點：隨機抽1~10項，每項最多買8個
        total_price = 0

        item_count = min(len(meals), 5)

        k = random.choices(list(range(1, item_count + 1)), weights=(100, 20, 5, 5, 1)[:item_count], k=1)[0]

        for m in random.sample(meals, k=k):
            count = random.choices(list(range(1, 5)), weights=(50, 40, 1, 1), k=1)[0]

            total_price += (count*m.price)
            item = OrderItem(meal_id=m.id, count=count, price=m.price, order_id=order.id)
            db.session.add(item)

        order.total_price = total_price
        db.session.add(order)
        db.session.flush()

    db.session.commit()

def add_bills():
    last_month_end = datetime.now().replace(day=1, hour=23, minute=59, second=59) - timedelta(days=1)
    orders = Order.query.with_entities(
            Order.user_id,
            func.sum(Order.total_price).label('total_price'),
            extract('year', Order.timestamp).label('year'),
            extract('month', Order.timestamp).label('month')
        )\
        .where(Order.timestamp <= last_month_end)\
        .group_by(Order.user_id, extract('year', Order.timestamp), extract('month', Order.timestamp))\
        .all()

    for o in orders:
        paid_datetime = None
        if is_paid := random.random() < 0.8:
            paid_datetime = datetime(o.year, o.month, 1,) + timedelta(days=31+random.randint(0, 14), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        bill = Bill(
            user_id=o.user_id,
            bill_month=date(o.year, o.month, 1),
            amount=o.total_price,
            is_paid=is_paid,
            paid_datetime=paid_datetime

        )
        db.session.add(bill)
    db.session.commit()