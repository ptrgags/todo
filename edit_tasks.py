from database import db

class EditTasks: 
    def __call__(self, args):
        props = {}

        if args.name:
            props['name'] = args.name

        if args.category:
            props['category'] = args.category

        db.update(props, eids=args.task_id)
