from datetime import datetime

from pony.orm import *
from pymysql.converters import decoders



class ORMFixture:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = "group_list"
        id = PrimaryKey(int, column="group_id")
        name = Optional(str, column="group_name")
        header = Optional(str, column="group_header")
        footer = Optional(str, column="group_footer")
        contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups", lazy=True)

    class ORMContact(db.Entity):
        _table_ = "addressbook"
        id = PrimaryKey(int, column="id")
        firstname = Optional(str, column="firstname")
        lastname = Optional(str, column="lastname")
        homephone = Optional(str, column="home")
        mobilephone = Optional(str, column="mobile")
        workphone = Optional(str, column="work")
        address = Optional(str, column="address")
        email = Optional(str, column="email")
        email2 = Optional(str, column="email2")
        email3 = Optional(str, column="email3")
        deprecated = Optional(bool, column="deprecated")
        groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def destroy(self):
        pass

    def convert_groups_to_model(self, groups):
        def convert_group(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert_group,groups))

    def convert_contacts_to_model(self, contacts):
        def convert_contact(contact):
            return Contact(id=str(contact.id), first_name=contact.firstname, last_name=contact.lastname,
                           address=contact.address, email=contact.email, email2=contact.email2, email3=contact.email3,
                           homephone=contact.homephone, mobilephone=contact.mobilephone,workphone=contact.workphone,
                           groups=self.convert_groups_to_model(contact.groups))
        return list(map(convert_contact,contacts))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if not c.deprecated))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORMContact if not c.deprecated and orm_group not in c.groups)
        )

    @db_session
    def get_contacts_with_groups(self):
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORMContact if not c.deprecated and c.groups)
        )