import imaplib
import os

here = os.path.abspath(os.path.dirname(__file__))
credentials = {}

with open(os.path.join(here[:here.find("simplgmail")-1], "dont_commit.py"), 'r', encoding='utf-8') as f:
    exec(f.read(), credentials)

username = credentials["username2"]
app_password = credentials["app_password2"]


imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, app_password)
