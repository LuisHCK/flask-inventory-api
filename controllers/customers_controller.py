from flask import request, jsonify
from database.database import Customer
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime


@jwt_required()
def index():
    customers = Customer.select()
    return list(p.to_dict() for p in customers)


@jwt_required()
def create():
    body = __whitelisted_params(request.json)
    body['user'] = current_user
    customer = Customer(**body)

    return customer.to_dict()


@jwt_required()
def show(id):
    customer = Customer.get(id=id)

    if customer:
        return customer.to_dict()

    return jsonify({"message": "Customer not found"}), 404


@jwt_required()
def update(id):
    customer = Customer.get(id=id)

    if customer:
        body = __whitelisted_params(request.json)
        body['updated_at'] = datetime.now()
        customer.set(**body)

        return customer.to_dict()

    return jsonify({"message": "Customer not found"}), 404


@jwt_required()
def destroy(id):
    customer = Customer.get(id=id)

    if customer:
        customer.delete()
        return {'message': 'Customer deleted'}

    return jsonify({"message": "Customer can't be deleted"}), 422


@jwt_required()
def customer_sales(id):
    customer = Customer.get(id=id)

    if customer:
        return list(sale.to_dict() for sale in customer.sales)

    return jsonify({"message": "Customer not found"}), 404


def __whitelisted_params(source):
    whitelist = [
        'name',
        'phone',
        'address',
    ]
    return dict((k, source[k]) for k in whitelist if k in source)
