from tasks import Task
from database import db

class DeleteTasks: 
    def prompt_confirmation(self, message):
        print(message + " (y/n) ", end='')
        answer = input()
        return answer.lower() == 'y'

    def delete_task(self, task):
        message = "Are you sure you want to delete {}".format(task)
        if self.prompt_confirmation(message):
            db.remove(eids=[task.eid])
            print("Deleted task {}".format(task))
    
    def delete_recursive(self, task):
        """
        Delete tasks recursively. Tasks that are not confirmed for deletion
        will become orphans.
        """
        # Delete tasks in 
        for subtask in task.subtasks:
            self.delete_recursive(subtask)

        # Delete the task after all children are deleted
        self.delete_task(task)

    def __call__(self, args):
        tasks = [Task(t) for t in db.all()]
        task_table = Task.build_task_table(tasks)

        for task in args.tasks:
            table_task = task_table.get(task.eid, None)
            if table_task:
                self.delete_recursive(table_task)
