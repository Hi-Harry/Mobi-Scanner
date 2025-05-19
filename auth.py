from functools import wraps
from flask import request, jsonify
import jwt
from models import User
from config import Config
from models import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['id'])
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated
