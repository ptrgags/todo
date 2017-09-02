from database import db

class DeleteTasks: 
    def prompt_confirmation(self, message):
        print(message + " (y/n) ", end='')
        answer = input()
        return answer.lower() == 'y'

    def __call__(self, args):
        for task in args.tasks:
            message = "Are you sure you want to delete {}".format(task)
            if self.prompt_confirmation(message):
                db.remove(eids=[task.eid])
                print("Deleted task {}".format(task))
