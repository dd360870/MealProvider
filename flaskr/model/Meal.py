from flaskr.db import db, Meal

def getAll():
    query = db.select(Meal)
    return db.session.execute(query).scalars()

def getById(id) -> Meal | None:
    query = db.select(Meal).where(Meal.id == id)
    return db.session.execute(query).scalar_one_or_none()
