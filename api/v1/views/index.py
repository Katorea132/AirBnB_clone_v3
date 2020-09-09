#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=["GET"])
def status():
    """Returns a status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"])
def stats():
    """Returns stats"""
    didi = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    return jsonify({k: storage.count(v) for k, v in didi.items()})
