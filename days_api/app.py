"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, request, jsonify

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


@app.post("/between")
def between():
    """Gets the days between two dates"""
    add_to_history(request)

    data = request.get_json()

    if not data or "first" not in data or "last" not in data:
        return jsonify({"error": "Missing required data."}), 400

    try:
        first = convert_to_datetime(data["first"])
        last = convert_to_datetime(data["last"])

    except ValueError:
        return jsonify({"error": "Unable to convert value to datetime."})

    days_between = get_days_between(first, last)

    return jsonify({"days": days_between})


@app.post("/weekday")
def weekday():
    """gets the day of the week"""

    add_to_history(request)

    data = request.get_json()

    if not data or "date" not in data:
        return jsonify({"error": "Missing required data."}), 400

    try:
        date_val = convert_to_datetime(data["date"])
    except ValueError:
        return jsonify({"error": "Unable to convert value to datetime."}), 400

    weekday = get_day_of_week_on(date_val)

    return jsonify({"weekday": weekday})


@app.get("/history")
def history():
    """Return API request history."""

    add_to_history(request)

    number = request.args.get("number", default=5)

    try:
        number = int(number)

        if number < 1 or number > 20:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "error": "Number must be an integer between 1 and 20."
        }), 400

    return jsonify(app_history[::-1][:number])


@app.delete("/history")
def delete_history():
    """Deletes all history"""

    clear_history()

    return jsonify({"status": "History cleared"})


@app.get("/current_age")
def current_age():
    """Return current age from birthdate."""

    date_parameter = request.args.get("date")

    if not date_parameter:
        return jsonify({"error": "Date parameter is required."}), 400

    try:
        birthdate = datetime.strptime(date_parameter, "%Y-%m-%d").date()

    except ValueError:
        return jsonify({"error": "Value for date parameter is invalid."}), 400

    current_age = get_current_age(birthdate)

    return jsonify({"current_age": current_age})


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
