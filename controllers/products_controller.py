from flask import request, jsonify
from database.database import Product
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime


@jwt_required()
def index():
	products = Product.select()
	return list(p.to_dict() for p in products)


@jwt_required()
def create():
	body = __whitelisted_params(request.json)
	body['user'] = current_user
	product = Product(**body)

	return product.to_dict()

@jwt_required()
def show(id):
	product = Product.get(id=id)

	if product:
		return product.to_dict()

	return jsonify({"message": "Product not found"}), 404

@jwt_required()
def update(id):
	product = Product.get(id=id)

	if product:
		body = __whitelisted_params(request.json)
		body['updated_at'] = datetime.now()
		product.set(**body)

		return product.to_dict()

	return jsonify({"message": "Product not found"}), 404

@jwt_required()
def destroy(id):
	product = Product.get(id=id)

	if product and current_user.role == 'admin':
		product.delete()
		return {'message': 'Product deleted'}

	return jsonify({"message": "Product can't be deleted"}), 422

# Cleanup request body and keep only safe fields
def __whitelisted_params(source):
	whitelist = [
		'name',
		'description',
		'photo',
		'brand',
		'unit',
		'content',
		'size',
		'color',
		'model',
		'warranty',
		'codebar'
	]
	return dict((k, source[k]) for k in whitelist if k in source)
