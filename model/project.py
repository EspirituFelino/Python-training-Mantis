

class Project:
    def __init__(self, id=None, name=None, status=None, global_categories=None, visibility=None, description=None):
        self.name = name
        self.id = id
        self.status = status
        self.global_categories = global_categories
        self.visibility = visibility
        self.description = description


    def __eq__(self, other):
        return ((self.id is None or other.id is None or self.id == other.id)
                and self.name == other.name)

    def __repr__(self):
        return f'{self.id}: {self.name}'