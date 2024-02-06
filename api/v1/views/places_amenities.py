#!/usr/bin/python3
"""
Defines route linking Places and Amenities resources
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request
from os import getenv


@app_views.route('places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenities(place_id):
    """
    Route amenities linked to the place with place_id
    """

    places = storage.all(Place)
    place_id = 'Place.' + place_id
    if place_id not in places:
        abort(404)

    amenities = [amenity.to_dict() for amenity in places[place_id].amenities]

    return jsonify(amenities), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def del_place_amenities(place_id, amenity_id):
    """
    Processes POST or DELETE request
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    meth = request.method
    data = request.get_json()

    if not place:
        abort(404)
    elif not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        if meth == 'DELETE':
            place.amenity_ids.remove(amenity)
        else:
            if not data:
                return jsonify({'error': 'Not a JSON'}), 400
            elif amenity.place_id == place_id:
                return jsonify(amenity.to_dict()) 200
            else:
                place.amenity_ids.append(amenity_id)
                place.save()
                return jsonify(amenity.to_dict()) 201
        place.save()
        return jsonify({}), 200
    else:
        if meth == 'DELETE':
            place.amenities.remove(amenity)
        else:
            if not data:
                return jsonify({'error': 'Not a JSON'}), 400
            elif amenity.place_id == place_id:
                return jsonify(amenity.to_dict()) 200
            else:
                place.amenities.append(amenity_id)
                place.save()
                return jsonify(amenity.to_dict()) 201
        place.save()
        return jsonify({}), 200
