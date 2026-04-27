

def test_login(app):
    app.session.ensure_logout()
    app.session.login(username="administrator", password="root")
    assert app.session.is_logged_in_as("administrator")