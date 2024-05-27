from flaskr.db import db, Meal

def get_price_by_id(id) -> int|None :
    query = db.select(Meal).where(Meal.id == id)
    meal = db.session.execute(query).scalar_one_or_none()
    if meal is None:
        return None
    else:
        return meal.price