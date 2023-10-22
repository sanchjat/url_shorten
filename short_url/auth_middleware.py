import os
from functools import wraps
import jwt
from flask import request, abort, jsonify
from flask import current_app
import models

SECRET_KEY = os.environ.get('SECRET_KEY') or 'sachin'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            })
        try:
            data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user=models.User().get_by_id(data["user_id"])
            if current_user is None:
                return jsonify({
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            })
            if not current_user["active"]:
                abort(403)
            # check token expiretime 
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            })

        return f(current_user, *args, **kwargs)

    return decorated