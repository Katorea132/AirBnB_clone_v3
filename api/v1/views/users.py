#!/usr/bin/python3
"""Module for cities"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User
from models.engine.db_storage import classes


viewer = "User"


@app_views.route("/users", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/users/<amenity_id>", methods=["GET"])
def guser(amenity_id=None):
    """GETs amenities or amenity id
    """
    if amenity_id:
        state = storage.get(viewer, amenity_id)
        if state:
            return jsonify(state.to_dict())
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([v.to_dict() for v in storage.all(viewer).values()])


@app_views.route("/users/<amenity_id>", methods=["DELETE"])
def duser(amenity_id):
    """DELETE states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def puser():
    """POST states
    """
    lili = ["email", "password"]
    retrieve = request.get_json(force=True, silent=True)
    if retrieve:
        for req in lili:
            if req in retrieve:
                continue
            abort(400, "Missing " + req)
        state = classes[viewer](**retrieve)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route("/users/<amenity_id>", methods=["PUT"])
def puuser(amenity_id):
    """PUTs states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        retrieve = request.get_json(force=True, silent=True)
        if retrieve:
            for k, v in retrieve.items():
                if k not in ["id", "created_at", "updated_at", "email"]:
                    setattr(state, k, v)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        abort(400, "Not a JSON")
    return make_response(jsonify({"error": "Not found"}), 404)
