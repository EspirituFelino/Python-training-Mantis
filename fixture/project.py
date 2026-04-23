

class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        wd.get("http://localhost/mantisbt-2.28.1/manage_proj_page.php")

    def go_to_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//span[text()=' Управление ']").click()
        wd.find_element_by_link_text("Проекты").click()


    def add_project(self, project):
        wd = self.app.wd
        self.go_to_projects_page()
        self.init_project_create()
        self.fill_project_form(project)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.app.change_id_field_value('project-name', project.name)
        self.app.change_id_field_value('project-description', project.description)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def init_project_create(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//button[text()='Создать новый проект']").click()

    def delete_project_by_id(self, project_id):
        wd = self.app.wd
        self.go_to_projects_page()
        self.open_id_project_page(project_id)
        wd.find_element_by_xpath("//button[contains(text(), 'Удалить проект')]").click()
        wd.find_element_by_css_selector("input[type='submit']").click()

    def open_id_project_page(self, project_id):
        wd = self.app.wd
        # wd.find_element_by_xpath(f'//a[contains(@href, "id={project_id}")]').click()
        element = wd.find_element_by_xpath(f'//a[contains(@href, "id={project_id}")]')
        wd.execute_script("arguments[0].click()", element)


    def delete_project_by_name(self, project_name):
        wd = self.app.wd
        self.go_to_projects_page()
        self.open_name_project_page(project_name)
        wd.find_element_by_xpath("//button[contains(text(), 'Удалить проект')]").click()
        wd.find_element_by_css_selector("input[type='submit']").click()

    def open_name_project_page(self, project_name):
        wd = self.app.wd
        # wd.find_element_by_xpath(f'//a[contains(text(), "{project_name}")]').click()
        element = wd.find_element_by_xpath(f'//a[contains(text(), "{project_name}")]')
        wd.execute_script("arguments[0].click()", element)
