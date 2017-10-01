import os

import pytest
from simplgmail.errors import InvalidInput
from simplgmail.models import GmailRequirements
from io import open


here = os.path.abspath(os.path.dirname(__file__))
credentials = {}

with open(os.path.join(here[:here.find("simplgmail")-1], "dont_commit.py"), 'r', encoding='utf-8') as f:
    exec(f.read(), credentials)

username = credentials["username"]
password = credentials["password"]
phone_number = credentials["phone_number"]
app_name = credentials["app_name"]


# these tests will all fail because I cannot enter terminal input
# google sends me a code that i will then need to input to the terminal,
# and pytest does not allow this
# how then to test?

# class TestSimplGmailRequirements:
#
#     # need actual username, password, and phone numbers to test
#     def test_disable_two_step_verification(self):
#         g = SimplGmailRequirements(username, password, phone_number)
#         g.disable_two_step_verification()
#         assert g.auth_enabled is False
#
#     def test_enable_two_step_verification(self):
#         g = SimplGmailRequirements(username, password, phone_number)
#         g.enable_two_step_verification()
#         assert g.auth_enabled is True
#
#     def test_generate_app_password(self):
#         g = SimplGmailRequirements(username, password, phone_number, app_name)
#         app_password = g.generate_app_password()
#         assert isinstance(app_password, str)
#         assert isinstance(g.app_password, str)
#
#     def test_remove_app_password(self):
#         g = SimplGmailRequirements(username, password, phone_number, app_name)
#         g.remove_app_password()
#         assert g.app_password is None
