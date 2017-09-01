from database import db

class DoneTask: 
    def __call__(self, args):
        for eid in args.task_id:
            record = db.get(eid=eid) 
            if args.uncheck:
                print("Unchecked task T{} - {}".format(eid, record['name']))
                db.update({'completed': False}, eids=[eid])
            else:
                print("Completed task T{} - {}".format(eid, record['name']))
                db.update({'completed': True}, eids=[eid])
