from flaskr.db import db, Order, OrderItem

def add_order(user_id, total_price, restaurant_id) -> Order:
    new_order = Order(
        user_id = user_id,
        total_price = total_price,
        paid = False,
        restaurant_id = restaurant_id
    )
    db.session.add(new_order)
    db.session.commit()

    return new_order
def create_order_items(order_id, order_details) -> None:
    for item in order_details:
        new_order_item = OrderItem(
            meal_id = item['meal_id'],
            count = item['count'],
            price = item['price'],
            order_id = order_id
        )
        db.session.add(new_order_item)
    db.session.commit()
def getAll() -> None:
    query = db.select(Order)
    return db.session.execute(query).scalars()

def delete_orders(order_list) -> None:
    for d_order_id in (order_list):
        order = Order.query.get_or_404(d_order_id)
        order_items = OrderItem.query.filter_by(order_id=d_order_id).all()
        for order_item in order_items:
            db.session.delete(order_item)
        db.session.delete(order)
    db.session.commit()