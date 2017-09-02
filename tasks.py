from database import db

class Task:
    def __init__(self, record):
        self.record = record
        self.subtasks = []

    @property
    def name(self):
        return self.record.get('name', '<Unnamed Task>')

    @property
    def eid(self):
        return self.record.eid

    @property
    def completed(self): 
        return self.record.get('completed', False)

    @property
    def category(self):
        return self.record.get('category', None)

    def format_label(self, with_category=True):
        if with_category:
            cat = "{}:".format(self.category) if self.category else ''
            return "T{} - {}{}".format(self.eid, cat, self.name)
        else:
            return "T{} - {}".format(self.eid, self.name)

    def __str__(self):
        return self.format_label()

    @classmethod
    def from_eid(cls, eid):
        record = db.get(eid=eid)
        return cls(record)
