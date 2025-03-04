from flask import Flask, jsonify, request
from supabase import create_client
import os
import jwt
import datetime

app = Flask(__name__)

# Supabase connection config
# database already exists
url = os.environ["DB_URL"]
key = os.environ["DB_KEY"]
client = create_client(url, key)

SECRET_KEY = os.environ["SECRET_KEY"]


def process_registration(deets_dict):
    """
    Dictionary argument contents:
    - "username": username
    - "password": hashed password
    """

    username = deets_dict["username"]
    password = deets_dict["password"]

    # invalid: empty username or pw given
    if username == "":
        return jsonify({"message": "Please input username"}), 400
    elif password == "":
        return jsonify({"message": "Please input password"}), 400

    # check if username taken
    user = client.table("users").select("*").eq("username", username).execute()
    if user.data:
        return jsonify({"message": "Username already taken"}), 400

    # if username available, make user account
    client.table("users").insert(
        {"username": username, "password": password}
    ).execute()
    return jsonify({"message": "Registration successful"}), 201


def process_login(deets_dict):
    """
    Dictionary argument contents:
    - "username": username
    - "password": hashed password
    """

    username = deets_dict["username"]
    password = deets_dict["password"]

    if username == "":
        return jsonify({"message": "Please input username"}), 400
    elif password == "":
        return jsonify({"message": "Please input password"}), 400

    user = client.table("users").select("*").eq("username", username).execute()

    if user.data and user.data[0]["password"] == password:
        token = jwt.encode(
            {
                "user_id": user.data[0]["id"],
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=1),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/register", methods=["POST"])
def register_user():
    # JSON data contains username and hashed password
    data = request.get_json()
    return process_registration(data)


@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    return process_login(data)
