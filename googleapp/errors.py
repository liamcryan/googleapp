

class InvalidInput(Exception):
    def __init__(self):
        Exception.__init__(self, "Sorry, your input doesn't look good.  "
                                 "Or, Maybe you've tried too many times and "
                                 "google thinks you aren't receiving the phone code?")
