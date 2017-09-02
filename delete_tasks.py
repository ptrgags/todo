from database import db

class DeleteTasks: 
    def prompt_confirmation(self, message):
        print(message + " (y/n) ", end='')
        answer = input()
        return answer.lower() == 'y'

    def __call__(self, args):
        for eid in args.task_id:
            record = db.get(eid=eid) 
            message = "Are you sure you want to delete T{} - {}?".format(
               eid,  record['name'])
            if self.prompt_confirmation(message):
                db.remove(eids=[eid])
                print("Deleted task T{} - {}".format(eid, record['name']))
