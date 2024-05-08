from flaskr.db import db, Restaurant

def getAll():
    query = db.select(Restaurant)
    return db.session.execute(query).scalars()

def getById(id) -> Restaurant | None:
    query = db.select(Restaurant).where(Restaurant.id == id)
    return db.session.execute(query).scalar_one_or_none()
