from database import db

class AddTask: 
    def __call__(self, args):
        for name in args.task_name:
            data = {
                'name': name,
                #'category': args.category,
                'completed': False,
                'parent': None
            }
            eid = db.insert(data)
            print('Added task T{}: {}'.format(eid, name))
