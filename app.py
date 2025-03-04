from flask import Flask, jsonify, request
from supabase import create_client
import os

app = Flask(__name__)

# Supabase connection config
# database already exists
url = os.environ["DB_URL"]
key = os.environ["DB_KEY"]
client = create_client(url, key)


def process_query(deets_dict):
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

    # check if uername taken
    user = client.table("users").select("*").eq("username", username).execute()
    if user.data:
        return jsonify({"message": "Username already taken"}), 400

    # if username available, make user account
    client.table("users").insert(
        {"username": username, "password": password}
    ).execute()
    return jsonify({"message": "Registration successful"}), 201


@app.route("/register", methods=["POST"])
def register_user():
    # JSON data contains username and hashed password
    data = request.get_json()
    return process_query(data)
