from utils.utils import process_registration
import json

# test setups
empty_username = ""
empty_password = ""

nonexistent_username = "nonexistent"

existing_username = "test_acc"
existing_password = "123"

wrong_password = "asdfghjkl"


def test_reject_no_username_supplied_when_registering():
    creds = json.dumps(
        {"username": empty_username, "password": existing_password}
    )
    response, status = process_registration(creds)
    assert "input username" in json.dumps(response)
    assert status == 400
