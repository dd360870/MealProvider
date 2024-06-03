from flaskr.db import db, MealReview

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

def get_comment_by_meal_id_and_user_id(meal_id, user_id) -> int|None :
    query = db.select(MealReview).where(MealReview.meal_id == meal_id and MealReview.user_id == user_id)
    review = db.session.execute(query).scalar_one_or_none()
    if review is None:
        return False
    else:
        return True

def getAll():
    query = db.select(MealReview)
    return db.session.execute(query).scalars()

def getById(id) -> MealReview | None:
    query = db.select(MealReview).where(MealReview.id == id)
    return db.session.execute(query).scalar_one_or_none()
