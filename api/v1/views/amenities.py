#!/usr/bin/python3
"""Module for cities"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.engine.db_storage import classes


viewer = "Amenity"


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def gamenities(amenity_id=None):
    """GETs amenities or amenity id
    """
    if amenity_id:
        state = storage.get(viewer, amenity_id)
        if state:
            return jsonify(state.to_dict())
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([v.to_dict() for v in storage.all(viewer).values()])


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def damenities(amenity_id):
    """DELETE states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def puamenities():
    """POST states
    """
    retrieve = request.get_json(force=True, silent=True)
    if retrieve:
        if "name" in retrieve:
            state = classes[viewer](**retrieve)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def pamenities(amenity_id):
    """PUTs states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        retrieve = request.get_json(force=True, silent=True)
        if retrieve:
            for k, v in retrieve.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        abort(400, "Not a JSON")
    return make_response(jsonify({"error": "Not found"}), 404)
