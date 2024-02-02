#!/usr/bin/python3
"""It’s time to start your API!"""
from flask import Flask
from models import *
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os

app = Flask(__name__)

"""Registering the blue print of appviews"""
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    declare a method to handle
    @app.teardown_appcontext that calls storage.close()
    """
    storage.close()


if __name__ == '__main__':
    """get the host env variable or use default"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
