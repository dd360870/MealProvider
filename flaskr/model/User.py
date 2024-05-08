from flaskr.db import db, User
from werkzeug.security import check_password_hash, generate_password_hash

def new(username, password) -> None:
    """Add new user

    Args:
        username (str): Username
        password (str): Password (raw)
    """

    new_user = User(
        username=username,
        password=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

def validate(username, password) -> User|None:
    """Validate user credential

    Args:
        username (str): Username
        password (str): Password (raw)
    """

    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalar_one_or_none()

    if user is None:
        return None
    elif not check_password_hash(user.password, password):
        return None

    return user

def getById(id) -> User|None:
    query = db.select(User).where(User.id == id)
    return db.session.execute(query).scalar_one_or_none()