from flask import Flask, request, jsonify
from utils.utils import process_registration, process_login
import json

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register_user():
    # JSON data contains username and hashed password
    data = json.dumps(request.get_json())
    msg, code = process_registration(data)
    return jsonify(msg), code


@app.route("/login", methods=["POST"])
def login_user():
    data = json.dumps(request.get_json())
    msg, code = process_login(data)
    return jsonify(msg), code
