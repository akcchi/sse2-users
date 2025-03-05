from flask import Flask, request
from utils import process_registration, process_login

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register_user():
    # JSON data contains username and hashed password
    data = request.get_json()
    return process_registration(data)


@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    return process_login(data)
