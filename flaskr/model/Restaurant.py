from flaskr.db import db, Restaurant, Meal, MealReview, OrderItem
from sqlalchemy.sql import func

def add():
    new_restaurant = Restaurant(
        name='新餐廳',
        description=None,
        tag='甜點',
        is_available=True
    )
    db.session.add(new_restaurant)

    db.session.commit()
    return new_restaurant.id

def hide(id):
    restaurant = Restaurant.query.get(id)

    restaurant.is_available=False

    db.session.commit()

def recover(id):
    restaurant = Restaurant.query.get(id)

    restaurant.is_available=True

    db.session.commit()

def update(id, name, tag):
    restaurant = Restaurant.query.get(id)

    restaurant.name = name
    restaurant.tag = tag
    db.session.commit()

def getAll():
    query = db.select(Restaurant).where(Restaurant.is_available == 1)
    restaurants = db.session.execute(query).scalars().all()
    if restaurants:
        for restaurant in restaurants:
            restaurant.average_stars, restaurant.review_count = restaurant_review_stars_count(restaurant)
    return restaurants

def getAllUnavailable():
    query = db.select(Restaurant).where(Restaurant.is_available == 0)
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
            restaurant.unavailable_meals = [meal for meal in restaurant.meals if meal.is_available == 0]
            restaurant.meals = [meal for meal in restaurant.meals if meal.is_available]
            for meal in restaurant.meals + restaurant.unavailable_meals:
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

def getByTagsUnavailable(tags: list[str]):
    if not tags:
        return getAllUnavailable()
    query = db.select(Restaurant).where((Restaurant.tag.in_(tags)) & (Restaurant.is_available == 0))
    restaurants = db.session.execute(query).scalars().all()
    if restaurants:
        for restaurant in restaurants:
            restaurant.average_stars, restaurant.review_count = restaurant_review_stars_count(restaurant)
    return restaurants

def change_restaurant_name(id, new_name):

    restaurant = db.session.get(Restaurant, id)
    if restaurant is None:
        raise ValueError(f"Restaurant with ID {id} not found.")

    restaurant.name = new_name
    db.session.commit()
