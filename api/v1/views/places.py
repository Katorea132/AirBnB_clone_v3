#!/usr/bin/python3
"""Module for cities"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.engine.db_storage import classes


viewer = "Place"
places = "City"


@app_views.route("/city/<amenity_id>/places", strict_slashes=False,
                 methods=["GET"])
def gcplace(amenity_id):
    """GETs amenities or amenity id
    """
    state = storage.get(places, amenity_id)
    if state:
        return jsonify([v.to_dict() for v in getattr(state, viewer)])
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/places/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def gpplace(amenity_id):
    """Gotta not forget the comment"""
    state = storage.get(viewer, amenity_id)
    if state:
        return jsonify(state.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/place/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def dplace(amenity_id):
    """DELETE states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<place_id>/places",
                 strict_slashes=False, methods=["POST"])
def pplacerevieew(place_id):
    """POST states
    """
    lili = ["name", "user_id"]
    retrieve = request.get_json(force=True, silent=True)
    if retrieve:
        state = storage.get(places, place_id)
        if not state:
            return make_response(jsonify({"error": "Not found"}), 404)
        for req in lili:
            if req in retrieve:
                continue
            abort(400, "Missing " + req)
        retrieve["places_id"] = place_id
        state = classes[viewer](**retrieve)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route("/places/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def puureview(amenity_id):
    """PUTs states
    """
    state = storage.get(viewer, amenity_id)
    if state:
        retrieve = request.get_json(force=True, silent=True)
        if retrieve:
            for k, v in retrieve.items():
                if k not in ["place_id", "created_at", "updated_at", "user_id",
                             "id"]:
                    setattr(state, k, v)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        abort(400, "Not a JSON")
    return make_response(jsonify({"error": "Not found"}), 404)
