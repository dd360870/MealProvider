from flaskr.db import db, Order, OrderItem

def getHistory(user_id):
    query = db.select(Order).where(Order.user_id == user_id)
    return db.session.execute(query).scalars()