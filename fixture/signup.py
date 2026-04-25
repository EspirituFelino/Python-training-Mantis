import re

class SignupHelper:
    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + 'signup_page.php')
        self.app.change_id_field_value('username', username)
        self.app.change_id_field_value('email-field', email)
        self.app.submit()

        mail = self.app.mail.get_mail(username, password, '[MantisBT] Account registration')
        url = self.extract_confirmation_url(mail)

        wd.get(url)
        self.app.change_id_field_value('password', password)
        self.app.change_id_field_value('password1', password)
        self.app.submit()

    def extract_confirmation_url(self, text):
        re.search("http://.*s", text).group(0)