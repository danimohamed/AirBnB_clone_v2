#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display a HTML page like 8-index.html"""
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    states = sorted(states, key=lambda state: state.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    places = sorted(places, key=lambda place: place.name)
    return render_template(
        '100-hbnb.html', states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_db(exception):
    """Close"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
