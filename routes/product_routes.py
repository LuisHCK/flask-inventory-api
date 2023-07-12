from flask import Blueprint
from controllers.products_controller import index, create, show, update, destroy

router = Blueprint('products_blueprint', __name__)
router.route('/', methods=['GET'])(index)
router.route('/', methods=['POST'])(create)
router.route('/<id>', methods=['GET'])(show)
router.route('/<id>', methods=['PATCH'])(update)
router.route('/<id>', methods=['DELETE'])(destroy)
