from typing import Annotated, List
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from core.database import *

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(200))
    price: Mapped[int]
    categorie_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))

    categories: Mapped[List["Categories"]] = relationship(back_populates="products")
    seller: Mapped["Seller"] = relationship(back_populates="products")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"))
    order_price: Mapped[int]
    count_of_products: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    buyer: Mapped["Buyer"] = relationship(back_populates="orders")
    products: Mapped[List["Product"]] = relationship(back_populates="orders")


class Buyer(Base):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    buyer_firstname: Mapped[str] = mapped_column(String(200))
    buyer_surname: Mapped[str] = mapped_column(String(200))
    registred_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    orders: Mapped[List["Order"]] = relationship(back_populates="buyers")


class Seller(Base):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_name: Mapped[str] = mapped_column(String(200))
    registred_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )

    products: Mapped[List["Product"]] = relationship(back_populates="sellers")


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    categorie_name: Mapped[str] = mapped_column(String(200))

    products: Mapped[List["Product"]] = relationship(back_populates="categories")