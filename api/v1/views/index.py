#!/usr/bin/python3
"""Index file"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    """return a json status OK"""
    return jsonify(status='OK'), 200, {'Content-Type': 'application/json'}