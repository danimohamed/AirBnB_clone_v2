#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states():
    """List states"""
    states = storage.all("State").values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def states_id(id):
    """Get state by id"""
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            state.cities = sorted(state.cities, key=lambda city: city.name)
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown_db(exception):
    """Close"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
