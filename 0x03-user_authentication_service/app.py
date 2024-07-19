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


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """ end point for profile """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return make_response(jsonify({"email": user.email}))
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> Response:
    """ end point for reset password token """

    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        resp = jsonify({"email": email, "reset_token": token})
        return make_response(resp)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password

    Return:
        - The user's password updated payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
