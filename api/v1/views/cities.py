#!/usr/bin/python3
"""city modules"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """using to_dict() to retrieve all city into a valid JSON"""
    cities = [city.to_dict() for city in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """retrieve cities id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(city_id):
    """delete state if the request require that"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """
    creating cities using POST
    an api that creates cities If the HTTP body
    request is not valid JSON, raise a 400 error
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """the funtion update city using PUT"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    """Updating the State object with all key-value pairs of the dictionary"""
    for key, value in data.items():
        """ignoring the created_at, updated_at, and id"""
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
