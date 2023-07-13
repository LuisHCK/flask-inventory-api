from flask import Blueprint

from controllers.auth_controller import login

router = Blueprint('auth_blueprint', __name__)

router.route('/login', methods=['POST'])(login)
