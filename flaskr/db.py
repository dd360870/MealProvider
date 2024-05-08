import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import SmallInteger, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    orders = relationship("Order", backref="user")

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    tag: Mapped[str] = mapped_column(String(128), nullable=True)

    meals = relationship("Meal", backref="restaurant")

class Meal(db.Model):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    price: Mapped[str] = mapped_column(Integer)
    restaurant_id = mapped_column(Integer, ForeignKey("restaurant.id"))

    reviews = relationship("MealReview", backref="meal")

class MealReview(db.Model):
    __tablename__ = "meal_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(String(1024), nullable=True)
    stars: Mapped[int] = mapped_column(SmallInteger)
    meal_id = mapped_column(Integer, ForeignKey("meal.id"))

class Order(db.Model):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    total_price: Mapped[int] = mapped_column(Integer)
    paid: Mapped[bool] = mapped_column(Boolean)

    items = relationship("OrderItem", backref="order")

class OrderItem(db.Model):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id = mapped_column(Integer, ForeignKey("meal.id"))
    count: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    order_id = mapped_column(Integer, ForeignKey("order.id"))
