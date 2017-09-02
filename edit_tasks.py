from database import db
from tasks import Task

class EditTasks: 
    def __call__(self, args):
        props = {}

        if args.name:
            props['name'] = args.name

        if args.category:
            props['category'] = args.category

        eids = [t.eid for t in args.tasks]
        db.update(props, eids=eids)

        for eid in eids:
            task = Task.from_eid(eid)
            print("Updated task {}".format(task))
