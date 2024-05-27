from flaskr.db import db, Restaurant, Meal, MealReview, OrderItem
from sqlalchemy.sql import func

def getAll():
    query = db.select(Restaurant)
    return db.session.execute(query).scalars()

def getById(id) -> Restaurant | None:
    query = (
        db.select(Restaurant)
        .where(Restaurant.id == id)
        .options(db.selectinload(Restaurant.meals))
    )
    restaurant = db.session.execute(query).scalar_one_or_none()

    if restaurant:
        for meal in restaurant.meals:
            meal.average_stars = calculate_average_stars(meal)
            meal.sales = get_meal_sales(meal)
   
    return restaurant

def calculate_average_stars(meal):
    return db.session.query(func.avg(MealReview.stars)).filter(MealReview.meal_id == meal.id).scalar()

def get_meal_sales(meal):
    total_sales = db.session.query(func.sum(OrderItem.count)).filter(OrderItem.meal_id == meal.id).scalar()
    if not total_sales:
        total_sales = 0
    return total_sales

def getByTag(tag: str):
    query = db.select(Restaurant).where(Restaurant.tag == tag)
    return db.session.execute(query).scalars()

def getByTags(tags: list[str]):
    if not tags:
        return getAll()
    query = db.select(Restaurant).where(Restaurant.tag.in_(tags))
    return db.session.execute(query).scalars()