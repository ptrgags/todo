from database import db

class Task:
    TRISTATE = 'maybe'

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
        if not self.subtasks:
            return self.record.get('completed', False)

        subtask_completion = [s.completed for s in self.subtasks]
        if all(s is True for s in subtask_completion):
            return True
        elif all(s is False for s in subtask_completion):
            return False
        else:
            return self.TRISTATE

    @property
    def category(self):
        return self.record.get('category', None)

    @property
    def parent_id(self):
        return self.record.get('parent', None)

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

    @classmethod
    def build_forest(cls, tasks):
        task_table = {t.eid: t for t in tasks}
        forest = []

        for task in tasks:
            if task.parent_id is None:
                # This is a standalone task so add it to the forest
                forest.append(task)
            elif task.parent_id not in task_table:
                # The parent task is hidden, so ignore this task
                continue
            else:
                # this is a subtask, so add it to the parent task
                task_table[task.parent_id].subtasks.append(task)

        return forest
