"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome messsage."""

    return jsonify({"message": "Welcome to the Days API."})


@app.get("/between")
def between():

    add_to_history(request)

    data = request.get_json()

    if not data or "first" not in data or "last" not in data:
        return jsonify({"error": True, "message": "Missing required data"}), 400

    try:
        first = convert_to_datetime(["first"])
        last = convert_to_datetime(["last"])

    except ValueError:
        return jsonify({"error": "Unable to convert value to datetime."})

    days_between = get_days_between(first, last)

    return jsonify({"days": days_between})


@app.post("/weekday")
def weekday():

    add_to_history(request)

    data = request.get_json()

    if not data or "date" not in data:
        return jsonify({"error": "Missing required data."}), 400

    try:
        date_val = convert_to_datetime(data["date"])
    except ValueError:
        return jsonify({"error": "Unable to convert to datetime,"}), 400

    weekday = get_day_of_week_on(date_val)

    return jsonify({"weekday": weekday})


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
