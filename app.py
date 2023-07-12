import os
from flask import Flask
from extensions import jwt, Pony
from routes.auth_route import auth_blueprint
from routes import product_routes
from database.database import db
from controllers.auth_controller import register_root_admin
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 24)))

    jwt.init_app(app)

    # Init database
    Pony(app)
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    
    # Register app routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(product_routes.router, url_prefix='/products')

    # Only if needed
    register_root_admin()

    return app