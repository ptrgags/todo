from database import db
from tasks import Task

class AddTasks: 
    def __call__(self, args):
        for name in args.task_name:
            data = {
                'name': name,
                'category': args.category,
                'completed': False,
                'parent': None
            }
            eid = db.insert(data)
            task = Task.from_eid(eid)
            print('Added task {}'.format(task))
