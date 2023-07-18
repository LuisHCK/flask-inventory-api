from flask import Blueprint
from controllers.sales_controller import index, create, show

router = Blueprint('sales_blueprint', __name__)
router.route('/', methods=["GET"])(index)
router.route('/', methods=["POST"])(create)
router.route('/<id>', methods=["GET"])(show)