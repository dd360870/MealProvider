from flaskr.db import db, Meal


def update(id, name, description, price):
    meal = Meal.query.get(id)

    meal.name = name
    meal.description = description
    meal.price = price

    db.session.commit()

def get_price_by_id(id) -> int|None :
    query = db.select(Meal).where(Meal.id == id)
    meal = db.session.execute(query).scalar_one_or_none()
    if meal is None:
        return None
    else:
        return meal.price

def getAll():
    query = db.select(Meal)
    return db.session.execute(query).scalars()

def getById(id) -> Meal | None:
    query = db.select(Meal).where(Meal.id == id)
    return db.session.execute(query).scalar_one_or_none()
