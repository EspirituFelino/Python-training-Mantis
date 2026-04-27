import ftplib
import importlib
import json
import os.path

import jsonpickle
import pytest
from fixture.application import Application
from fixture.orm import ORMFixture
import ftputil

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file_path) as config_file:
            target = json.load(config_file)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config["web_admin"]["username"], password=config["web_admin"]["password"])

    return fixture

@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")

@pytest.fixture(scope="session")
def db(request, config):
    db_config = config["db"]
    db_fixture = ORMFixture(host=db_config["host"], name=db_config["name"],
                           user=db_config["user"], password=db_config["password"])
    def fin():
        db_fixture.destroy()
    request.addfinalizer(fin)
    return db_fixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    request.addfinalizer(fin)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            test_data = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])
        elif fixture.startswith("json_"):
            test_data = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])

def load_from_module(module):
    return importlib.import_module(f"data.{module}").test_data

def load_from_json(json_file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{json_file}.json")) as json_data:
        return jsonpickle.decode(json_data.read())

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        # добавить config_inc в resources
        if remote.path.isfile('config_inc.php.bak'):
            remote.remove('config_inc.php.bak')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc.php.bak')
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc.php.bak'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
            remote.rename('config_inc.php.bak', 'config_inc.php')

