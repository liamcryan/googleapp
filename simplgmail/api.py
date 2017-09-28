from simplgmail.models import GmailSMTP, GmailIMAP, SimplGmailRequirements


def smtp(username, app_password):
    return GmailSMTP(username, app_password)


def imap(username, app_password):
    return GmailIMAP(username, app_password)


def generate_app_pass(username, password, phone_number, app_name):
    s = SimplGmailRequirements(username, password, phone_number, app_name)
    s.generate_app_password()


def remove_app_pass(username, password, phone_number, app_name):
    s = SimplGmailRequirements(username, password, phone_number, app_name)
    s.remove_app_password()


def enable_two_step_auth(username, password, phone_number):
    s = SimplGmailRequirements(username, password, phone_number)
    s.enable_two_step_verification()


def disable_two_step_auth(username, password):
    s = SimplGmailRequirements(username, password)
    s.disable_two_step_verification()
