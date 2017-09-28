----------
simplgmail
----------

Requirements
------------

1.  Enable 2-Step Authentication

2.  Generate an App Password

You also must have a google account :)

Automatic
---------

*This process uses selenium & chromedriver, so I think you need to have chrome installed*

Into command prompt type:

$ pip install simplgmail

Into Python type:

>>> import simplgmail
>>> my_app_password = simplgmail.app_password("your_gmail_username", "your_gmail_password", "your_phone_number")

*Note: you will be prompted mid-execution on the command prompt for phone verification codes!*

Manual
------

If you don't want to try the automatic method or it isn't working, you can try the manual method.  If the
automatic method worked for you, then skip this section.

- Go here and follow directions for enabling 2 step authentication:

    - https://support.google.com/accounts/answer/185839?hl=en

- Then go to the link below and follow directions for generating an app password:

    - https://support.google.com/accounts/answer/185833?hl=en


Did it work?
------------

After that you can make sure everything worked by typing into Python:

>>> import smtplib
>>> s = smtplib.SMTP('smtp.gmail.com:587')
>>> s.ehlo()
>>> s.starttls()
>>> s.login(username, app_password)

*Note: make sure to use the app password you just generated when you login!*

You should see something that looks like this if it worked:

>>> (235, b'2.7.0 Accepted')

The next thing to check is this:

>>>  import imaplib
>>> m = imaplib.IMAP4_SSL("imap.gmail.com")
>>> m.login(username, app_password)

You should see something that looks like this:

>>> ('OK', [b'{} authenticated (Success)'.format(username)])

Now you are ready!  Be sure to remember that if you want to run your program on another computer,
you will need to generate another app password.


Usage
-----

>>> import simplgmail
>>>
>>> s = simplgmail.smtp(username, app_password)
>>> s.send(sender, receiver, message)  # this should send your email to receiver(s)
>>>
>>> m = simplgmail.imap(username, app_password)
>>> m.set("INBOX")
>>> _id = m.search(subject="Daily Adventures")
>>> email = m.fetch(_id)  # email should now contain the content of the email associated with _id


Testing
-------

Not very far here, but coming.