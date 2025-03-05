from utils.utils import process_registration, process_login
import json
import hashlib

# test setups
empty_username = ""
empty_password = ""

nonexistent_username = "nonexistent"
nonexistent_password = "asdfghjkl"

existing_username = "test_acc"
existing_password = "123"

# get password hash
sha256_hash = hashlib.sha256()
sha256_hash.update(existing_password.encode("utf-8"))
hashed_existing_password = sha256_hash.hexdigest()

sha256_hash2 = hashlib.sha256()
sha256_hash2.update(nonexistent_password.encode("utf-8"))
hashed_nonexistent_password = sha256_hash2.hexdigest()


def test_reject_no_username_supplied_when_registering():
    creds = json.dumps(
        {
            "username": empty_username,
            "hashedPassword": hashed_nonexistent_password,
        }
    )
    response, status = process_registration(creds)
    assert "input username" in json.dumps(response)
    assert status == 400


def test_reject_no_password_supplied_when_registering():
    creds = json.dumps(
        {"username": nonexistent_username, "hashedPassword": empty_password}
    )
    response, status = process_registration(creds)
    assert "input password" in json.dumps(response)
    assert status == 400


def test_cannot_reuse_taken_username_for_registration():
    creds = json.dumps(
        {
            "username": existing_username,
            "hashedPassword": hashed_nonexistent_password,
        }
    )
    response, status = process_registration(creds)
    assert "Username already taken" in json.dumps(response)
    assert status == 400


def test_reject_no_username_on_login():
    creds = json.dumps(
        {
            "username": empty_username,
            "hashedPassword": hashed_existing_password,
        }
    )
    response, status = process_login(creds)
    assert "input username" in json.dumps(response)
    assert status == 400


def test_reject_no_password_on_login():
    creds = json.dumps(
        {"username": existing_username, "hashedPassword": empty_password}
    )
    response, status = process_login(creds)
    assert "input password" in json.dumps(response)
    assert status == 400
