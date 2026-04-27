from model.project import Project


def test_add_project(app, db):
    # app.session.ensure_login(username="administrator", password="root")
    old_projects = db.get_project_list()
    project = Project(name=app.random_string('Name', 5), description=app.random_string('Description', 5))
    app.project.add_project(project)
    old_projects.append(project)
    new_projects = db.get_project_list()
    assert old_projects == new_projects
