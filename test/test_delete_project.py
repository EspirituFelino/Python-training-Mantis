import random

from model.project import Project


def test_delete_project(app, db):
    # app.session.ensure_login(username="administrator", password="root")
    old_projects = db.get_project_list()
    if len(old_projects) == 0:
        app.project.add_project(Project(name='Burn After Read'))
        old_projects = db.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    old_projects.remove(project)
    new_projects = db.get_project_list()
    assert old_projects == new_projects
    assert not app.soap.check_project_by_name(project.name)
