from flask import Blueprint
from controllers.customers_controller import (
    index,
    create,
    show,
    update,
    destroy,
    customer_sales
)

router = Blueprint("customer_blueprint", __name__)
router.route("/", methods=["GET"])(index)
router.route("/", methods=["POST"])(create)
router.route("/<id>", methods=["GET"])(show)
router.route("/<id>", methods=["PATCH"])(update)
router.route("/<id>", methods=["DELETE"])(destroy)
router.route("/<id>/sales", methods=["GET"])(customer_sales)
