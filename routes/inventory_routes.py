from flask import Blueprint
from controllers.inventories_controller import (
    index,
    create,
    show,
    update,
    destroy,
    list_inventory_products,
    create_inventory_product,
    update_inventory_product,
    delete_inventory_product,
)


router = Blueprint("inventory_blueprint", __name__)
router.route("/", methods=["GET"])(index)
router.route("/", methods=["POST"])(create)
router.route("/<id>", methods=["GET"])(show)
router.route("/<id>", methods=["PATCH"])(update)
router.route("/<id>", methods=["DELETE"])(destroy)
router.route("/<id>/products", methods=["GET"])(list_inventory_products)
router.route("/<id>/products", methods=["POST"])(create_inventory_product)
router.route("/<inventory_id>/products/<product_id>", methods=["PATCH"])(
    update_inventory_product
)
router.route("/<inventory_id>/products/<product_id>", methods=["DELETE"])(
    delete_inventory_product
)
