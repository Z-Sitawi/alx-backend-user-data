#!/usr/bin/env python3
""" Module for basic Flask app. """
from auth import Auth
from flask import (Flask, jsonify, request, abort, make_response,
                   Response, redirect)

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def welcome():
    """ Simple welcome route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def create_user():
    """ end point for creating a new user"""
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """ end point for log in"""
    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        json_resp = jsonify({"email": email, "message": "logged in"}), 200
        response = make_response(json_resp)
        response.set_cookie("session_id", AUTH.create_session(email))
        return response

    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """ end point for log out """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
