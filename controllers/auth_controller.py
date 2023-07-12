import os
from flask import request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager
from extensions import jwt
from database.database import User
from pony.orm import db_session
from bcrypt import hashpw, checkpw, gensalt

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
@db_session
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User[identity]
    return user


# Authenticate user with usernamer and password
# Returns a signed jwtoken if validation passess
def login():
    body = request.json
    print(body['username'])
    user = User.get(username=body['username'])

    if user:
        password_matches = __checkpw(body['password'], user.password_digest)

        if password_matches:
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token)
    
    return jsonify({"message": "Username or password invalid"}), 401


def __hash_password(plainpwd):
    password = bytes(plainpwd, encoding='utf-8')
    salt_rounds = os.getenv('SALT_ROUNDS', 12)
    salt = gensalt(int(salt_rounds))
    hashed = hashpw(password, salt)
    return hashed.decode('utf-8')

def __checkpw(password, hash):
    return checkpw(
        bytes(password, encoding='utf-8'),
        bytes(hash, encoding='utf-8')
    )


@db_session
def register_root_admin():
    total_users = User.select().count()
    if total_users == 0:
        password = __hash_password(os.getenv('ROOT_PASSWORD'))
        root_user = User(
            firstname='Root',
            lastname='User',
            username=os.getenv('ROOT_USERNAME'),
            password_digest=password,
            role='admin'
        )
