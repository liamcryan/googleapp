import imaplib
import os
import smtplib

""" This file can accompany this post: http://data-handyman.com/post/python-gmail2/ """


def get_credentials():
    """ credentials for using imaplib and smtplib with Gmail """
    here = os.path.abspath(os.path.dirname(__file__))
    credentials = {}
    # the credentials are stored in a file called dont_commit.py which looks like:
    # username2="my username"
    # app_password2="my app password"
    # if gmail_python_part_2.py is here:  /somewhere/googleapp/googleapp/gmail_python_part_2.py
    # then put the dont_commit.py file in the same directory as the 'somewhere' directory
    with open(os.path.join(here[:here.find("googleapp")], "dont_commit.py"), 'r', encoding='utf-8') as f:
        exec(f.read(), credentials)

    username = credentials["username2"]
    app_password = credentials["app_password2"]
    return username, app_password


def get_formspree_email_info():

    username, app_password = get_credentials()

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, app_password)

    imap.select("Formspree")

    message = imap.fetch(b'1', '(RFC822)')

    msg = str(message[1][0][1])
    a = msg.find("name:\\r\\n")
    b = msg.find("email:\\r\\n")
    c = msg.find("subject:\\r\\n")
    d = msg.find("message:\\r\\n")

    name = msg[a+len('name:\\r\\n'):b-len('\\r\\n\\r\\n\\r\\n')]
    email = msg[b+len('email:\\r\\n'):c-len('\\r\\n\\r\\n\\r\\n')]
    subject = msg[c+len('subject:\\r\\n'):d-len('\\r\\n\\r\\n\\r\\n')]

    return name, email, subject


def send_email_to_contactor(name, email, subject):

    username, app_password = get_credentials()

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username, app_password)

    send_to = email
    send_subject = subject
    send_name = name

    message = "Subject:{}\n\nHi {}, thanks for your email.  " \
              "I'll be getting back to you shortly and look forward to talking with you".format(send_subject, send_name)

    s.sendmail(from_addr="data.handyman.01@gmail.com", to_addrs=send_to, msg=message)


if __name__ == "__main__":
    info_tuple = get_formspree_email_info()
    send_email_to_contactor(*info_tuple)