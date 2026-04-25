import pkg_resources

def test_sighup_new_account(app):
    username = app.random_letters("user_", 6)
    email = username + '@localhost'
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)
    app.session.logout()

