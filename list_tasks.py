from database import db

class ListTasks: 
    def format_task(self, task):
        check = 'x' if task['completed'] else ' '
        tid = 'T{}'.format(task.eid)
        return "- [{}] {} {}".format(check, tid, task['name'])

    def __call__(self, args): 
        for task in db.all():
            print(self.format_task(task))
