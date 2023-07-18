from datetime import datetime
from decimal import Decimal
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True, index='idx_user__username')
    role = Required(str, default="user")
    firstname = Required(str)
    lastname = Required(str)
    phone = Optional(str)
    photo = Optional(str)
    created_at = Optional(datetime, default=lambda: datetime.now())
    updated_at = Optional(datetime, default=lambda: datetime.now())
    products = Set('Product')
    sales = Set('Sale')
    inventories = Set('Inventory')
    customers = Set('Customer')
    password_digest = Required(
        str, hidden=True, index='idx_user__password_digest')


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    photo = Optional(str)
    brand = Optional(str)
    unit = Optional(str)
    content = Optional(str)
    size = Optional(str)
    color = Optional(str)
    model = Optional(str)
    warranty = Optional(str)
    codebar = Required(str, unique=True, index='idx_product__codebar')
    inventory_products = Set('InventoryProduct')
    user = Required(User)
    sale_products = Set('SaleProduct')
    created_at = Optional(
        datetime, default=lambda: datetime.now(), index='idx_product__created_at')
    updated_at = Optional(datetime, default=lambda: datetime.now())


class Inventory(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    description = Optional(str)
    inventory_products = Set('InventoryProduct')
    user = Required(User)
    created_at = Optional(
        datetime, default=lambda: datetime.now(), index='idx_inventory__created_at')
    updated_at = Optional(datetime, default=lambda: datetime.now())


class InventoryProduct(db.Entity):
    id = PrimaryKey(int, auto=True)
    purchase_price = Required(Decimal, precision=2)
    stock = Required(int, size=16)
    product = Required(Product)
    inventory = Required(Inventory)
    sale_price = Required(Decimal, precision=2)
    created_at = Optional(datetime, default=lambda: datetime.now(
    ), index='idx_inventory_product__created_at')
    updated_at = Optional(datetime, default=lambda: datetime.now())


class Sale(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    sale_products = Set('SaleProduct')
    customer = Optional('Customer')
    status = Required(str, default='completed', index='idx_sale__status')
    payment_reference = Optional(str)
    notes = Optional(str)
    payment_type = Optional(str, default="cash")
    created_at = Optional(
        datetime, default=lambda: datetime.now(), index='idx_sale__created_at')
    updated_at = Optional(datetime, default=lambda: datetime.now())


class SaleProduct(db.Entity):
    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    sale = Required(Sale)
    price = Required(Decimal, precision=2)
    quantity = Required(int, size=16)
    discount = Optional(Decimal, precision=2)


class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, index="idx_customer__name")
    phone = Optional(str)
    address = Optional(str)
    sales = Set(Sale)
    user = Set(User)
    created_at = Optional(
        datetime, default=lambda: datetime.now(), index='idx_customer__created_at')
    updated_at = Optional(datetime, default=lambda: datetime.now())
