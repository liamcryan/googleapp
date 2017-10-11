---------
googleapp
---------

Want to create a Google App Password?  Or enable Google's 2-Step Authentication?
You've come to the right place.  This library uses Selenium to automate browser interaction, but you
don't see it thanks to chrome headless.


Generate Google App Password
----------------------------

>>> import googleapp
>>> app_pass = googleapp.generate_app_pass(username, password, phone_number, app_name)

You'll receive a verification code on your phone.  When you are prompted , make sure to type the code in
the terminal.

Remove a Google App Password
----------------------------

>>> googleapp.remove_app_pass(username, password, phone_number, app_name)


Enable Google's 2 Step Authentication
-------------------------------------

>>> googleapp.enable_two_step_auth(username, password, phone_number)


Disable Google's 2 Step Authentication
--------------------------------------

>>> googleapp.disable_two_step_auth(username, password, phone_number)


Problems
--------

1.  Two step authentication provides the user a couple of options to verify.  One method is to verify
by entering a received phone code.  The other method is to verify by Google console.  This library
will not work if you have the verify by Google Console enabled.  This is something I will work on
soon.

2.  Within the library is a /drivers/chromedriver.exe file.  This is the chromedriver executable which
works specifically with Windows.  I plan on including the chromedriver executable for other operating
systems and hopefully the library will be able to know which one to use.  That is also something I
will need to work on.

3.  I'm not sure how to run a test suite  because I don't think I can enter terminal input mid execution.
Maybe I can get the phone code from a Twilio phone number?  I'll have to look into it.
