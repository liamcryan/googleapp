----------
simplgmail
----------

Want to use Python to interact with Gmail?  Cool.  You now need to enable 2-step authentication or
allow "less secure apps" within Google.  But not manually, just do this:

>>> import simplgmail
>>> app_pass = simplgmail.generate_app_pass(username, password, phone_number, app_name)

You'll receive a verification code on your phone.  When you are prompted, make sure to type in the code.

Now, you're ready to interact with Gmail!  P.S.  I hope the above command worked for you!  Make sure to save the app
password, because you will need it below.  If you forget to save the app password, just do:

>>> simplgmail.remove_app_pass(username, password, phone_number, app_name)

Then run (and make sure to save it this time):

>>> app_pass = simplgmail.generate_app_pass(username, password, phone_number, app_name)


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

I'm not sure how to run a test suite for SimplGmailRequirements (automatically generating the app password) because
I can't enter terminal input mid execution.

Haven't tested GmailSMTP or GmailIMAP

Installation
------------

Not very confident with this yet, so only installation is through this github repo.
