from flaskr.db import db, Meal, MealReview, Restaurant

def newReview(user_id, meal_id, stars, content) -> None:
    """Add new review

    Args:
        stars (int): Stars
        content (str): Content (raw)
    """

    new_review = MealReview(
        user_id = user_id,
        meal_id = meal_id,
        stars=stars,
        content=content
    )
    db.session.add(new_review)
    db.session.commit()

def recover(id):
    meal = Meal.query.get(id)

    meal.is_available=True

    db.session.commit()

def hide(id):
    meal = Meal.query.get(id)

    meal.is_available=False

    db.session.commit()

def add(restaurant_id, name, description, price):

    new_meal = Meal(
        name=name,
        price=price,
        description=description,
        restaurant_id=restaurant_id,
        is_available=True
    )
    db.session.add(new_meal)

    db.session.commit()

    last_restaurant = Restaurant.query.order_by(Restaurant.id.desc()).first()
    return last_restaurant.id

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
