from dataclasses import dataclass
from core.database import Base
from core.models import Product, Order, Buyer, Seller, Categories

@dataclass
class Tables:
    Product = Product
    Order = Order
    Buyer = Buyer
    Seller = Seller
    Categories = Categories