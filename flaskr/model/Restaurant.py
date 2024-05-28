from flaskr.db import db, Restaurant, Meal, MealReview, OrderItem
from sqlalchemy.sql import func

def getAll():
    query = db.select(Restaurant).where(Restaurant.is_available == 1)
    restaurants = db.session.execute(query).scalars().all()
    if restaurants:
        for restaurant in restaurants:
            restaurant.average_stars, restaurant.review_count = restaurant_review_stars_count(restaurant)
    return restaurants

def getById(id) -> Restaurant | None:
    query = (
        db.select(Restaurant)
        .where(Restaurant.id == id)
        .options(db.selectinload(Restaurant.meals))
    )

    with db.session.no_autoflush:
        restaurant = db.session.execute(query).scalar_one_or_none()
        if restaurant:
            restaurant.meals = [meal for meal in restaurant.meals if meal.is_available]
            for meal in restaurant.meals:
                meal.average_stars, meal.review_count = meal_review_stars_count(meal)
                meal.sales = get_meal_sales(meal)
    return restaurant

def restaurant_review_stars_count(restaurant):
    average_stars, review_count = (
        db.session.query(func.avg(MealReview.stars), func.count(MealReview.id))
        .join(Meal, MealReview.meal_id == Meal.id)
        .filter(Meal.restaurant_id == restaurant.id)
        .one()
    )
    return average_stars, review_count

def meal_review_stars_count(meal):
    average_stars, review_count = (
        db.session.query(func.avg(MealReview.stars), func.count(MealReview.id))
        .filter(MealReview.meal_id == meal.id)
        .one()
    )
    return average_stars, review_count

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
    query = db.select(Restaurant).where((Restaurant.tag.in_(tags)) & (Restaurant.is_available == 1))
    restaurants = db.session.execute(query).scalars().all()
    if restaurants:
        for restaurant in restaurants:
            restaurant.average_stars, restaurant.review_count = restaurant_review_stars_count(restaurant)
    return restaurants