#!/usr/bin/python3
"""state modules"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
