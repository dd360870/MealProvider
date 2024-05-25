import random
from datetime import datetime, timedelta
from flaskr.db import db
import flaskr.db as orm

def random_datetime():
    # 範圍：一年前到今天
    sdate = datetime.now()-timedelta(days=365)
    random_ts = random.randint(round(sdate.timestamp()), round(datetime.now().timestamp()))
    random_dt = datetime.fromtimestamp(random_ts).strftime("%Y-%m-%d %H:%M:%S")
    return random_dt

def add_orders():

    meals = orm.Meal.query.all()
    users = orm.User.query.all()

    if len(users) == 0:
        raise Exception("Please insert \"User\" table first.")

    if len(meals) == 0:
        raise Exception("Please insert \"Meal\" table first.")

    for _ in range(100):
        order = orm.Order(total_price=0, timestamp=random_datetime(), user_id=random.choice(users).id)

        # make sure order has id
        db.session.add(order)
        db.session.flush()

        # 餐點：隨機抽1~10項，每項最多買8個
        total_price = 0
        k = random.choices(list(range(1, 6)), weights=(100, 20, 5, 5, 1), k=1)[0]
        for m in random.choices(meals, k=k):
            count = random.choices(list(range(1, 5)), weights=(50, 40, 1, 1), k=1)[0]

            total_price += (count*m.price)
            item = orm.OrderItem(meal_id=m.id, count=count, price=m.price, order_id=order.id)
            db.session.add(item)

        order.total_price = total_price
        db.session.add(order)
        db.session.flush()

    db.session.commit()