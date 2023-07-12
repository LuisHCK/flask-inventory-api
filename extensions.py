from flask_jwt_extended import JWTManager
from pony.flask import Pony

jwt = JWTManager()
pony = Pony