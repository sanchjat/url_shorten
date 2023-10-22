from flask import Blueprint, request, redirect, jsonify

from short_url.models import Url
from short_url.utils import prep_response, handle_500
from short_url.auth_middleware import token_required

urls_blueprint = Blueprint("urls", __name__)

PREFIX = "http://localhost:5000/"  # "http://sho.rt/"


@urls_blueprint.route("/url", methods=["POST"])
@handle_500
@token_required
def generate_url(user):
    """This will create short url for give url"""
    original_url = request.json["original_url"]
    # TODO validate URL is in correct formate like
    # http://abc.com/mypage?p=2
    url = Url()
    short_key = url.create_short_url({"original_url": original_url})
    return jsonify({"short_url": PREFIX + short_key})


@urls_blueprint.route("/<short_key>", methods=["GET"])
@handle_500
def fetch_url(short_key):
    """This will check short key in DB if present
    It will redirect to original URL otherwise throw 404"""

    if not short_key:
        return prep_response("Wrong short URL.", 404)

    url = Url()
    response = url.find_by_short_key(short_key)
    if response and response.get("original_url"):
        return redirect(response["original_url"])

    return prep_response("Wrong short URL.", 404)
