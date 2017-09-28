import os

import pytest
from simplgmail.errors import InvalidInput
from simplgmail.models import SimplGmailRequirements
from io import open


here = os.path.abspath(os.path.dirname(__file__))
credentials = {}

with open(os.path.join(here[:here.find("simplgmail")-1], "dont_commit.py"), 'r', encoding='utf-8') as f:
    exec(f.read(), credentials)

username = credentials["username"]
password = credentials["password"]
phone_number = credentials["phone_number"]
app_name = credentials["app_name"]


class TestSimplGmailRequirements:

    def test_sign_in_error_username_1(self):
        with pytest.raises(InvalidInput):
            g = SimplGmailRequirements("", "aasdf", "8888888")
            g.sign_in()

    def test_sign_in_error_username_2(self):
        with pytest.raises(InvalidInput):
            g = SimplGmailRequirements("123;;;pl,;", "asdf", "8888888")
            g.sign_in()

    def test_sign_in_error_password_1(self):
        with pytest.raises(InvalidInput):
            g = SimplGmailRequirements("data.handyman.01", "asdf", "8888888")
            g.sign_in()

    def test_sign_in_error_password_2(self):
        with pytest.raises(InvalidInput):
            g = SimplGmailRequirements("data.handyman.01", "notmypassword", "8888888")
            g.sign_in()

    # need actual username, password, and phone numbers to test below
    def test_disable_two_step_verification(self):
        g = SimplGmailRequirements(username, password, phone_number)
        g.disable_two_step_verification()
        assert g.auth_enabled is False

    def test_disable_two_step_verification_again(self):
        g = SimplGmailRequirements(username, password, phone_number)
        g.disable_two_step_verification()
        assert g.auth_enabled is False

    def test_enable_two_step_verification(self):
        g = SimplGmailRequirements(username, password, phone_number)
        g.enable_two_step_verification()
        assert g.auth_enabled is True

    def test_enable_two_step_verification_again(self):
        g = SimplGmailRequirements(username, password, phone_number)
        g.enable_two_step_verification()
        assert g.auth_enabled is True

    def test_generate_app_password(self):
        g = SimplGmailRequirements(username, password, phone_number, app_name)
        g.generate_app_password()

    def test_remove_app_password(self):
        g = SimplGmailRequirements(username, password, phone_number, app_name)
        g.remove_app_password()