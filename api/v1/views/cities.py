#!/usr/bin/python3
"""Module for cities"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State
from models.engine.db_storage import classes


viewer = "State"
specific = "City"
param = "cities"


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def gstaterc(state_id):
    """GETs states or a state id and its cities
    """
    state = storage.get(viewer, state_id)
    if state:
        return jsonify([v.to_dict() for v in getattr(state, param)])
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<city_id>", methods=["GET"])
def gcitier(city_id):
    """GETs city by id
    """
    city = storage.get(specific, city_id)
    if city:
        return jsonify(city.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def dcitier(city_id):
    """DELETE cities
    """
    city = storage.get(specific, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def pcities(state_id):
    """POST cities in states
    """
    retrieve = request.get_json(force=True, silent=True)
    if retrieve:
        state = storage.get(viewer, state_id)
        if not state:
            return make_response(jsonify({"error": "Not found"}), 404)
        if "name" in retrieve:
            retrieve["state_id"] = state_id
            state = classes[specific](**retrieve)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=["PUT"])
def pucitier(city_id):
    """PUTs cities
    """
    state = storage.get(specific, city_id)
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
