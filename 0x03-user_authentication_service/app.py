#!/usr/bin/env python3
""" Module for basic Flask app. """
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response

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


@app.route('/sessions', methods=['POST'])
def login():
    """ end point for log in"""
    email = request.form['email']
    password = request.form['password']

    if Auth.valid_login(email=email, password=password):
        json_resp = jsonify({"email": email, "message": "logged in"}), 200
        response = make_response(json_resp)
        response.set_cookie("session_id", Auth.create_session(email))
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
