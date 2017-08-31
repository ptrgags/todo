from database import db

class AddTask: 
    def __call__(self, args):
        category = args.category if args.category else "_default"
        table = db.table('category')

        for name in args.task_name:
            data = {'name': name}
            eid = table.insert(data)
            print('Added task T{}: {}'.format(eid, name))
