from tinydb import Query
from database import db
from tasks import Task
from colors import color

class ListTasks: 
    CHECK_MARK = color('✓', fg='green')
    COLOR_BRACKETS = 208
    COLOR_DONE = 239 # grey in ANSI 256-color mode
    COLOR_LABEL = 208

    def format_task(self, task):
        """
        Format a task like

        - [ ] T1 - Uncompleted task

        or

        - [x] T2 - Completed task
        """
        checkbox_left = color('- [', fg=self.COLOR_BRACKETS)
        checkbox_right = color(']', fg=self.COLOR_BRACKETS)
        check = self.CHECK_MARK if task.completed else ' '
        task_str = task.format_label(with_category=False)
        task_color = self.COLOR_DONE if task.completed else 'white'
        task_str = color(task_str, fg=task_color)
        return "{}{}{} {}".format(
            checkbox_left, check, checkbox_right, task_str)

    def fetch_tasks(self, show_all):
        if show_all:
            return db.all()
        else:
            TaskTable = Query()
            return db.search(TaskTable.completed != True)

    def bucket_categories(self, tasks):
        by_category = {}
        for record in tasks:
            task = Task(record)
            by_category.setdefault(task.category, []).append(task)
        return by_category

    def __call__(self, args):
        tasks = self.fetch_tasks(args.show_all)
        by_category = self.bucket_categories(tasks)

        # Print default category tasks first
        default_tasks = by_category.pop(None, [])
        if default_tasks:
            for task in default_tasks:
                print(self.format_task(task))
            print()

        # Print the rest of the tasks
        for cat in sorted(by_category):
            label = color(cat + ":", fg=self.COLOR_LABEL)
            print(label)
            for task in by_category[cat]:
                print(self.format_task(task))
            print()
