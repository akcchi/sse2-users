from flask import jsonify
from supabase import create_client
import os
import datetime
import jwt

# Supabase connection config
# database already exists
url = os.environ["DB_URL"]
key = os.environ["DB_KEY"]
client = create_client(url, key)

SECRET_KEY = os.environ["SECRET_KEY"]


def process_registration(user_creds):
    """
    JSON argument contents:
    - "username": username
    - "password": hashed password
    """

    username = user_creds["username"]
    password = user_creds["password"]

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


def process_login(user_creds):
    """
    JSON argument contents:
    - "username": username
    - "password": hashed password
    """

    username = user_creds["username"]
    password = user_creds["password"]

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
