from flask import request, jsonify
from database.database import Inventory, InventoryProduct
from flask_jwt_extended import jwt_required, current_user
from pony.orm import sum
from datetime import datetime

@jwt_required()
def index():
	inventories = list()

	for inventory in Inventory.select():
		inventories.append({ **inventory.to_dict(), 'total_products': sum(inventory.inventory_products) })

	return inventories


@jwt_required()
def create():
	body = __whitelisted_params(request.json)
	body['user'] = current_user
	inventory = Inventory(**body)
	return inventory.to_dict()


@jwt_required()
def show(id):
	inventory = Inventory.get(id=id)

	if inventory:
		return inventory.to_dict()

	return jsonify({"message": "Inventory not found"}), 404


@jwt_required()
def update(id):
	inventory = Inventory.get(id=id)

	if inventory:
		body = __whitelisted_params(request.json)
		body['updated_at'] = datetime.now()
		inventory.set(**body)
		return inventory.to_dict()

	return jsonify({"message": "Inventory not found"}), 404


@jwt_required()
def destroy(id):
	inventory = Inventory.get(id=id)

	if inventory and current_user.role == 'admin':
		inventory.delete()
		return {'message': 'Inventory deleted'}

	return jsonify({"message": "Inventory can't be deleted"}), 422


@jwt_required()
def list_inventory_products(id):
	inventory = Inventory.get(id=id)
	products = list()

	for inventory_product in inventory.inventory_products:
		products.append(inventory_product.product.to_dict())

	return products


@jwt_required()
def create_inventory_product(id):
	body = __whitelisted_params(request.json)
	body['inventory'] = id

	if InventoryProduct.select(product=body['product'], inventory=id).count() > 0:
		return {'message': 'Already added'}, 422

	inventory_product = InventoryProduct(**body).to_dict(related_objects=True)

	return {
		**inventory_product,
		'product': inventory_product['product'].to_dict(),
		'inventory': inventory_product['inventory'].to_dict()
	}


@jwt_required()
def update_inventory_product(inventory_id, product_id):
	body = __whitelisted_params(request.json)
	inventory_product = InventoryProduct.select(inventory=inventory_id, product=product_id).first()

	print(inventory_product)

	if inventory_product:
		inventory_product.set(**body)
		inventory_product = inventory_product.to_dict(related_objects=True)

		return {
			**inventory_product,
			'product': inventory_product['product'].to_dict(),
			'inventory': inventory_product['inventory'].to_dict()
		}
	
	return jsonify({"message": "Inventory Product relationship not found"}), 422


def __whitelisted_params(source):
	whitelist = [
		'purchase_price',
		'stock',
		'product',
		'sale_price'
	]

	return dict((k, source[k]) for k in whitelist if k in source)
