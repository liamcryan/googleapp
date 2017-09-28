import os
from io import open

from simplgmail import SimplGmailRequirements

here = os.path.abspath(os.path.dirname(__file__))
credentials = {}

with open(os.path.join(here[:here.find("simplgmail")-1], "dont_commit.py"), 'r', encoding='utf-8') as f:
    exec(f.read(), credentials)

username = credentials["username"]
password = credentials["password"]
phone_number = credentials["phone_number"]
app_name = credentials["app_name"]

g = SimplGmailRequirements(username, password, phone_number, app_name)
g.generate_app_password()
print("stop")