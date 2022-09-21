from itertools import count
from typing import Dict, List
from unicodedata import name
from pydantic import BaseModel


class CharacteristicItem(BaseModel):
    name: str
    value: str


class Login(BaseModel):
    username: str
    password: str


class BuyProduct(BaseModel):
    id: int
    selected: int


class Buy(Login):
    products: List[BuyProduct]


class Characteristics(BaseModel):
    items: List[CharacteristicItem]

class OrderCreate(BaseModel):
    user_id: int
    products: List[BuyProduct]

class ProductBase(BaseModel):
    name: str
    price: int
    count: int
    description: str
    characteristics: Characteristics
    image: str


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
