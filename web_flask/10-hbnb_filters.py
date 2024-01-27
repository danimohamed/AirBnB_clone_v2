#!/usr/bin/python3
"""This module starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display a HTML page like 6-index.html"""
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    states = sorted(states, key=lambda state: state.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return render_template(
        '10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """Close"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
