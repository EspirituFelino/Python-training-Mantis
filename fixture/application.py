import random
import string
from selenium import webdriver

from fixture.orm import ORMFixture
from fixture.project import ProjectHelper
from fixture.session import SessionHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError(f"Invalid browser {browser}")
        self.wd.implicitly_wait(0.3)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def destroy(self):
        self.wd.quit()


    def open_home_page(self):
        if not self.wd.current_url == 'http://localhost/mantisbt-2.28.1/my_view_page.php':
            self.wd.get(self.base_url)

    def change_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_id_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_id(field_name).click()
            wd.find_element_by_id(field_name).clear()
            wd.find_element_by_id(field_name).send_keys(text)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def random_string(self, prefix, maxlen):
        symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
        return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])