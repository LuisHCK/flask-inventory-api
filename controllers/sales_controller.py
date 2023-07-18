from flask import request, jsonify
from database.database import Inventory, Product, Sale, SaleProduct, Customer
from flask_jwt_extended import jwt_required, current_user
from pony.orm import sum, rollback
from datetime import datetime


@jwt_required()
def index():
    sales = Sale.select()
    return list(p.to_dict() for p in sales)


@jwt_required()
def create():
    body = __whitelisted_params(request.json)
    sale_products = request.json.get("sale_products", list())
    body['user'] = current_user

    # Create sale object
    sale = Sale(**body)

    # Find or create customer
    customer = None
    customer_data = request.json.get("customer")

    if isinstance(customer_data, int):
        customer = Customer[customer_data]
    elif isinstance(customer_data, str):
        customer = Customer(name=customer_data)
    elif isinstance(customer_data, dict):
        customer = Customer(**customer_data)

    if customer:
        sale.customer = customer

    # Register sale_products
    sale_products = list()
    sale.flush()

    try:
        for item in request.json["sale_products"]:
            sale_products.append(SaleProduct(**item, sale=sale.id).to_dict())
    except:
        rollback()
        return {"message": "Can't save sale_products"}, 422

    res = sale.to_dict(related_objects=True)

    return {
        **res,
        "customer": res['customer'].to_dict(),
        "sale_products": sale_products,
        "user": res["user"].to_dict()
    }


@jwt_required()
def show(id):
    sale = Sale.get(id=id)

    if sale:
        return sale.to_dict()

    return jsonify({"message": "Sale not found"}), 404


@jwt_required()
def update(id):
    sale = Sale.get(id=id)

    if sale:
        return jsonify({"message": "Sales can't be deleted"}), 422
    return jsonify({"message": "Sale not found"}), 404


@jwt_required()
def destroy(id):
    return jsonify({"message": "Sales can't be deleted"}), 422


def __whitelisted_params(source):
    whitelist = [
        "payment_reference",
        "payment_type",
        "status",
        "notes"
    ]

    return dict((k, source[k]) for k in whitelist if k in source)
