from database import db

class DoneTasks: 
    def __call__(self, args):
        for task in args.tasks:
            if args.uncheck:
                print("Unchecked task {}".format(task))
                db.update({'completed': False}, eids=[task.eid])
            else:
                print("Completed task {}".format(task))
                db.update({'completed': True}, eids=[task.eid])
