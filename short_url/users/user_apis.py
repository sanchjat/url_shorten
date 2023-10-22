# -*- coding: utf-8 -*-

import jwt
import os
from flask import Blueprint, request, jsonify

from datetime import datetime

from short_url.models import User
from short_url.utils import prep_response, handle_500

users_blueprint = Blueprint("users", __name__)

SECRET_KEY = os.environ.get("SECRET_KEY") or "sachin"


def validate_email_and_password(*args):
    return True


@users_blueprint.route("/users/login", methods=["POST"])
@handle_500
def login():

    data = request.json
    if not data:
        return prep_response("Please provide user details", 400)

    # validate input
    is_validated = validate_email_and_password(
        data.get("email"),
        data.get("password")
        )
    if is_validated is not True:
        return prep_response("Invalid Data", 400)

    user = User().login(data["email"], data["password"])
    if user:
        try:
            # Token should expire after 24 hrs
            user["token"] = jwt.encode(
                {"user_id": user["_id"], "created_at": str(datetime.now())},
                SECRET_KEY,
                algorithm="HS256",
            )
            return jsonify(
                {"message": "Successfully fetched auth token",
                 "token": user["token"]}
            )
        except Exception as e:
            return prep_response("Something went wrong" + e, 500)
    return prep_response("Error fetching auth token!,\
                         invalid email or password", 400)
