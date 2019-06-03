from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int
    category: str


@dataclass
class CartItem:
    product_id: int
    quantity: int


@dataclass
class Order:
    id: int
    user_id: int
    items: List[CartItem]
    total: float
    status: str
    created_at: str
