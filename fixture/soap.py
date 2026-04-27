from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.client = Client("http://localhost/mantisbt-2.28.1/api/soap/mantisconnect.php?wsdl")


    def can_login(self, username, password):
        # client = Client("http://localhost/mantisbt-2.28.1/api/soap/mantisconnect.php?wsdl")
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def check_project_by_name(self, project_name):
        try:
            prj_id = self.client.service.mc_project_get_id_from_name('administrator', 'root', project_name)
            if prj_id != 0:
                return True
            else:
                try:
                    self.client.service.mc_project_get_categories('administrator', 'root', prj_id)
                    return True
                except WebFault:
                    return False
        except WebFault:
            return False