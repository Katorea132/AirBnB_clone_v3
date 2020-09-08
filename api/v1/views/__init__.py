#!/usr/bin/python3
"""Initializer for this module
"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint("app_vies", __name__, url_prefix="/api/v1")
