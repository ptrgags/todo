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
            
        '''
        for name in args.task_name:
            data = {
                'name': name,
                'category': args.category,
                'optional': False,
                'completed': False,
                'parent': None
            }
            eid = db.insert(data)
            print('Added task T{}: {}'.format(eid, name))
        '''
