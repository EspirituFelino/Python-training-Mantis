from datetime import datetime

from pony.orm import *
from pymysql.converters import decoders

from model.project import Project


class ORMFixture:

    db = Database()

    class ORMProject(db.Entity):
        _table_ = "mantis_project_table"
        id = PrimaryKey(int, column="id")
        name = Optional(str, column="name")
        description = Optional(str, column="description")

    # class ORMGroup(db.Entity):
    #     _table_ = "group_list"
    #     id = PrimaryKey(int, column="group_id")
    #     name = Optional(str, column="group_name")
    #     header = Optional(str, column="group_header")
    #     footer = Optional(str, column="group_footer")
    #     contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups", lazy=True)
    #
    # class ORMContact(db.Entity):
    #     _table_ = "addressbook"
    #     id = PrimaryKey(int, column="id")
    #     firstname = Optional(str, column="firstname")
    #     lastname = Optional(str, column="lastname")
    #     homephone = Optional(str, column="home")
    #     mobilephone = Optional(str, column="mobile")
    #     workphone = Optional(str, column="work")
    #     address = Optional(str, column="address")
    #     email = Optional(str, column="email")
    #     email2 = Optional(str, column="email2")
    #     email3 = Optional(str, column="email3")
    #     deprecated = Optional(bool, column="deprecated")
    #     groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def destroy(self):
        pass

    def convert_projects_to_model(self, projects):
        def convert_project(project):
            return Project(id=str(project.id), name=project.name, description=project.description)
        return list(map(convert_project,projects))

    @db_session
    def get_project_list(self):
        return self.convert_projects_to_model(select(g for g in ORMFixture.ORMProject))
