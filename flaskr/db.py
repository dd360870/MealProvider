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
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    orders = relationship("Order", backref="user")
    reviews = relationship("MealReview", backref="user")

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    tag: Mapped[str] = mapped_column(String(128), nullable=True)

    meals = relationship("Meal", backref="restaurant")

class Meal(db.Model):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    price: Mapped[str] = mapped_column(Integer, nullable=False)
    restaurant_id = mapped_column(Integer, ForeignKey("restaurant.id"), nullable=False)

    reviews = relationship("MealReview", backref="meal")

class MealReview(db.Model):
    __tablename__ = "meal_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(String(1024), nullable=True)
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    meal_id = mapped_column(Integer, ForeignKey("meal.id"), nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

class Order(db.Model):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)

    items = relationship("OrderItem", backref="order")

class OrderItem(db.Model):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id = mapped_column(Integer, ForeignKey("meal.id"), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    order_id = mapped_column(Integer, ForeignKey("order.id"), nullable=False)

    meal = relationship("Meal")
