from database import db
from tasks import Task

class MakeSubtasks: 
    def __call__(self, args):
        parent = args.parent
        for name in args.task_name:
            data = {
                'name': name,
                'category': parent.category,
                'completed': False,
                'parent': parent.eid
            }
            eid = db.insert(data)
            task = Task.from_eid(eid)
            print('Added subtask {} to task {}'.format(task, parent))
