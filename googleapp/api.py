from googleapp.models import GoogleApp


def generate_app_pass(username, password, phone_number, app_name):
    s = GoogleApp(username, password, phone_number, app_name)
    s.generate_app_password()


def remove_app_pass(username, password, phone_number, app_name):
    s = GoogleApp(username, password, phone_number, app_name)
    s.remove_app_password()


def enable_two_step_auth(username, password, phone_number):
    s = GoogleApp(username, password, phone_number)
    s.enable_two_step_verification()


def disable_two_step_auth(username, password):
    s = GoogleApp(username, password)
    s.disable_two_step_verification()
