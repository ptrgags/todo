from tasks import Task
from database import db

class DoneTasks: 
    def check_task(self, task, uncheck):
        """
        Check off/uncheck a leaf node by setting the `completed` property
        """
        if uncheck:
            print("Unchecked task {}".format(task))
            db.update({'completed': False}, eids=[task.eid])
        else:
            print("Completed task {}".format(task))
            db.update({'completed': True}, eids=[task.eid]) 

    def done_recursive(self, task, uncheck):
        """
        Recursively check/uncheck tasks.
        """
        if not task.subtasks:
            self.check_task(task, uncheck)
        else:
            for subtask in task.subtasks:
                self.done_recursive(subtask, uncheck)

    def __call__(self, args):
        # Construct the task forest
        tasks = [Task(t) for t in db.all()]
        task_table = Task.build_task_table(tasks)

        for task in args.tasks:
            table_task = task_table.get(task.eid, None)
            if table_task:
                self.done_recursive(table_task, args.uncheck)
