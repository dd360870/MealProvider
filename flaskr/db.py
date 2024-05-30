import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import SmallInteger, Integer, String, DateTime, Boolean, ForeignKey, Date, Index, UniqueConstraint, text
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from typing import List, Optional

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
    is_clerk: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
    restaurant_id = mapped_column(Integer, ForeignKey('restaurant.id'), nullable=True)

    restaurant = relationship("Restaurant")
    orders = relationship("Order", backref="user")
    reviews = relationship("MealReview", backref="user")
    bills: Mapped[Optional["Bill"]] = relationship(back_populates="user")

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

    reviews: Mapped[Optional["MealReview"]] = relationship(back_populates="meal")

class MealReview(db.Model):
    __tablename__ = "meal_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(1024), nullable=True)
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey("meal.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    meal: Mapped["Meal"] = relationship(back_populates="reviews")

class Order(db.Model):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    restaurant_id = mapped_column(Integer, ForeignKey("restaurant.id"), nullable=False)

    items = relationship("OrderItem", backref=backref("order", cascade="all, delete-orphan", single_parent=True))

class OrderItem(db.Model):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id = mapped_column(Integer, ForeignKey("meal.id"), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    order_id = mapped_column(Integer, ForeignKey("order.id"), nullable=False)

    meal = relationship("Meal")

class Bill(db.Model):
    __tablename__ = "bill"

    __table_args__ = (
        UniqueConstraint("user_id", "bill_month", name="user_month_constraint"),
        Index("user", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    bill_month: Mapped[datetime.date] = mapped_column(Date, nullable=False, comment="結帳月份")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="結帳金額")
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否已結帳")
    paid_datetime: Mapped[datetime.date] = mapped_column(DateTime, nullable=True, comment="結帳時間")

    user: Mapped["User"] = relationship(back_populates="bills")

