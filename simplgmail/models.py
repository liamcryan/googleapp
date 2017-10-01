import os

import imaplib
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from simplgmail.errors import InvalidInput


class GmailSMTP:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.smtp = smtplib.SMTP('smtp.gmail.com:587')
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(username, password)

    def tear_down(self):
        self.smtp.quit()
        self.smtp = None

    def send(self, sender, receiver, message, subject=None, file_name=None):
        """

        :param sender: a string email address like "liam@data-handyman.com"
        :param receiver: a string email address or a list of string email addresses
        :param message: a string
        :param subject: a string, not required
        :param file_name: a text file name (don't know if it could open other files...haven't tested)
        :return:
        """
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject if subject else "Email Headed Your Way"
        msg.attach(MIMEText(message, "plain"))

        text = msg.as_string()

        if file_name:
            attachment = open(file_name, "rb")

            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename={}".format(file_name))

            msg.attach(part)

        self.smtp.sendmail(from_addr=sender, to_addrs=receiver, msg=text)


class GmailIMAP:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(username, password)

    def tear_down(self):
        self.imap.close()
        self.imap.logout()
        self.imap = None

    def set(self, label):
        r, d = self.imap.select(label)
        if r == "NO":
            raise Exception(d)

    def search(self, subject="ALL"):
        if subject == "ALL":
            r, d = self.imap.uid("search", None, subject)
        else:
            r, d = self.imap.uid("search", None, '(HEADER Subject {})'.format(subject))
        if r == "OK":
            return d.split()[-1]

    def fetch(self, _id):
        if not isinstance(_id, bytes):
            _id = str.encode(_id)
        r, d = self.imap.uid("fetch", _id, "(RFC822)")
        if r == "OK":
            return d
        raise Exception(d)

    def delete(self, _id):
        if not isinstance(_id, bytes):
            _id = str.encode(_id)
        self.imap.uid("store", _id, "+FLAGS", "\\Deleted")
        self.imap.expunge()


class GmailRequirements:
    def __init__(self, username, password, phone_number=None, app_name=None):
        here = os.path.abspath(os.path.dirname(__file__))
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=os.path.join(here, "drivers", "chromedriver"),
                                       chrome_options=chrome_options)
        self.auth_enabled = None
        self.signed_in = False
        self.app_password = None
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.app_name = app_name

    def tear_down(self):
        self.driver.quit()  # self.driver.close() closes the currently open tab
        self.auth_enabled = False
        self.signed_in = False
        self.app_password = None

    @staticmethod
    def _receive_code():
        return input("please enter the verification code  --> ")

    def _check_valid_input(self):
        try:  # aria-invalid='true'
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, "//input[@aria-invalid='true']")))
            raise InvalidInput
        except TimeoutException:
            return

    def _username(self):
        username = self.driver.find_element_by_id("identifierId")
        username.clear()
        username.send_keys(self.username)
        go_to_next = self.driver.find_element_by_id("identifierNext")
        go_to_next.click()

        self._check_valid_input()

    def _password(self):
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='password']")))
        password.clear()
        password.send_keys(self.password)
        go_to_next = self.driver.find_element_by_id("passwordNext")
        go_to_next.click()

        self._check_valid_input()

    def _phone_code(self):
        try:
            phone_code = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "idvPin")))
        except TimeoutException:
            self.auth_enabled = False
            return None
        phone_code.clear()
        phone_code.send_keys(self._receive_code())
        go_to_next = self.driver.find_element_by_id("idvPreregisteredPhoneNext")
        go_to_next.click()
        self.auth_enabled = True  # this must be true because you are inputting a phone code
        self._check_valid_input()

    def sign_in(self):
        self.driver.get(
            "https://accounts.google.com/"
            "signin/v2/identifier?hl=en&passive=true&continue="
            "https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        if "v2" not in self.driver.current_url:
            raise Exception("Can only authenticate v2 of Google's sign in page")
        self._username()
        self._password()
        self._phone_code()  # what about the case where the user just needs to tap the phone?
        self.signed_in = True

    def _turn_off_auth(self):
        turn_off = self.driver.find_element_by_xpath("//span[contains(text(), 'Turn off')]")
        turn_off.click()
        turn_off_popup = self.driver.find_elements_by_xpath("//span[contains(text(), 'Turn off')]")[2]
        turn_off_popup.click()
        self.auth_enabled = False

    def disable_two_step_verification(self):
        if not self.signed_in:
            self.sign_in()
        if self.auth_enabled is False:
            return None
        self.driver.get("https://myaccount.google.com/signinoptions/two-step-verification")
        self._password()
        self._turn_off_auth()

    def _enter_number(self):
        try:
            phone_number = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        except TimeoutException:
            return None  # this is the case where the phone number is already saved...
        phone_number.clear()
        phone_number.send_keys(self.phone_number)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        go_to_next = self.driver.find_element_by_xpath("//span[contains(text(), 'Next')]")
        go_to_next.click()
        self._check_valid_input()

    def _confirm_phone(self):
        try:
            confirm_phone = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        except TimeoutException:  # this is the case where the phone number is already saved
            return None
        confirm_phone.send_keys(self._receive_code())
        go_to_next = self.driver.find_element_by_xpath("//span[contains(text(), 'Next')]")
        go_to_next.click()
        self._check_valid_input()

    def _turn_on_auth(self):
        turn_on = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Turn on')]")))
        turn_on.click()
        self.auth_enabled = True

    def enable_two_step_verification(self):
        if not self.signed_in:
            self.sign_in()
        if self.auth_enabled:
            return None
        self.driver.get("https://myaccount.google.com/signinoptions/two-step-verification/enroll-welcome")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        get_started = self.driver.find_element_by_xpath("//span[contains(text(), 'Get started')]")
        get_started.click()
        self._password()
        self._enter_number()
        self._confirm_phone()
        self._turn_on_auth()

    def _app_password_enter_info(self):
        self._password()
        # self._phone_code()  # not sure if i need this

        # none of this works...need to figure out how to click on menu and select item i want...
        select_app = self.driver.find_element_by_xpath("//content[contains(text(), 'Select app')]")
        select_app.click()
        # WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located(
        # (By.XPATH, "//div[@aria-label='Mail'")))
        # mail_option = self.driver.find_elements_by_xpath("//div[@aria-label='Mail'")[2]
        # mail_option.click()
        time.sleep(2)
        self.driver.execute_script('document.querySelectorAll(\'[aria-label="Mail"]\')[1].click()')

        select_device = self.driver.find_element_by_xpath("//content[contains(text(), 'Select device')]")
        select_device.click()
        # WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located(
        #     (By.XPATH, "//div[@aria-label='Other (Custom name)'")))
        # other_custom_name = self.driver.find_elements_by_xpath("//div[@aria-label='Other (Custom name)'")[3]
        # other_custom_name.click()
        time.sleep(2)
        self.driver.execute_script('document.querySelectorAll(\'[aria-label="Other (Custom name)"]\')[2].click()')

        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        other_input = self.driver.find_element_by_tag_name("input")
        other_input.clear()
        other_input.send_keys(self.app_name)

        generate = self.driver.find_element_by_xpath("//span[contains(text(), 'Generate')]")
        generate.click()

        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Your app password for your device')]/following-sibling::div")))
        app_password = self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Your app password for your device')]/following-sibling::div").text
        self.app_password = app_password
        return app_password

    def generate_app_password(self):
        if not self.signed_in:
            self.sign_in()
        if not self.auth_enabled:
            self.enable_two_step_verification()

        self.driver.get("https://myaccount.google.com/apppasswords")  # it's like this gets skipped over...

        self._app_password_enter_info()  # may need to retry this if there is an error

    def _app_password_remove_info(self):
        self._password()
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@data-name='{}']/div[2]/div")))
        except TimeoutException:
            self.app_password = None
            return None
        trash_app_name = self.driver.find_element_by_xpath(
            "//div[@data-name='{}']/div[2]/div".format(self.app_name))
        trash_app_name.click()
        self.app_password = None

    def remove_app_password(self):
        if not self.signed_in:
            self.sign_in()
        self.driver.get("https://myaccount.google.com/apppasswords")
        self._app_password_remove_info()
