from tinydb import Query
from database import db
from tasks import Task
from colors import color

class ListTasks: 
    CHECK_MARK = color('✓', fg='green')
    TRISTATE = color('■', fg='yellow')
    COLOR_BRACKETS = 208
    COLOR_DONE = 239 # grey in ANSI 256-color mode
    COLOR_LABEL = 208 # orange
    COLOR_TASK_ARROW = 57 # Saturated purple
    COLOR_SUBTASK_ARROW = 48 # mint green

    def format_completed_status(self, task):
        if task.completed == Task.TRISTATE:
            return self.TRISTATE
        elif task.completed is True:
            return self.CHECK_MARK
        else:
            return ' '

    def format_task_label(self, task):
        """
        Format a task like

        - [ ] T1 - Uncompleted task

        or

        - [x] T2 - Completed task
        """
        checkbox_left = color('[', fg=self.COLOR_BRACKETS)
        checkbox_right = color(']', fg=self.COLOR_BRACKETS)
        check = self.format_completed_status(task)

        task_str = task.format_label(with_category=False)
        task_color = self.COLOR_DONE if task.completed is True else 'white'
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
        for task in tasks:
            by_category.setdefault(task.category, []).append(task)
        return by_category

    def print_category(self, category):
        label = color(category + ":", fg=self.COLOR_LABEL)
        print(label)

    def prefix_lines(self, lines, first_prefix, rest_prefix, fg=None):
        first, *rest = lines

        yield color(first_prefix, fg=fg) + first

        for line in rest:
            yield color(rest_prefix, fg=fg) + line

    def format_middle_subtask(self, task):
        lines = self.format_subtasks(task)
        yield from self.prefix_lines(
            lines, ' ├─> ', ' │   ', self.COLOR_SUBTASK_ARROW)

    def format_last_subtask(self, task):
        lines = self.format_subtasks(task)
        yield from self.prefix_lines(
            lines, ' └─> ', '     ', self.COLOR_SUBTASK_ARROW)

    def format_subtasks(self, task):
        yield self.format_task_label(task)
        if task.subtasks:
            *middle, last = task.subtasks

            for subtask in middle:
                yield from self.format_middle_subtask(subtask)

            yield from self.format_last_subtask(last)


    def print_single_task(self, task):
        lines = self.format_subtasks(task)
        prefixed = self.prefix_lines(
            lines, '═══> ', '     ', self.COLOR_TASK_ARROW)
        for line in prefixed:
            print(line)
    
    def print_first_task(self, task):
        lines = self.format_subtasks(task)
        prefixed = self.prefix_lines(
            lines, '═╦═> ', ' ║   ', self.COLOR_TASK_ARROW)
        for line in prefixed:
            print(line)
    
    def print_middle_task(self, task):
        lines = self.format_subtasks(task)
        prefixed = self.prefix_lines(
            lines, ' ╠═> ', ' ║   ', self.COLOR_TASK_ARROW)
        for line in prefixed:
            print(line)

    def print_last_task(self, task):
        lines = self.format_subtasks(task)
        prefixed = self.prefix_lines(
            lines, ' ╚═> ', '     ', self.COLOR_TASK_ARROW)
        for line in prefixed:
            print(line)

    def print_task_forest(self, tasks):
        if len(tasks) == 1:
            self.print_single_task(tasks[0])
        elif len(tasks) >= 2:
            first, *middle, last = tasks
            self.print_first_task(first)
            for task in middle:
                self.print_middle_task(task)
            self.print_last_task(last)
        print()

    def category_filter(self, buckets, categories):
        if categories:
            return {
                cat: task 
                for cat, task in buckets.items() 
                if cat in categories}
        else:
            return buckets
        

    def __call__(self, args):
        tasks = [Task(record) for record in self.fetch_tasks(args.show_all)]
        task_trees = Task.build_forest(tasks)
        by_category = self.bucket_categories(task_trees)
        by_category = self.category_filter(by_category, args.category)

        # Print default category tasks first
        default_tasks = by_category.pop(None, [])
        if default_tasks:
            self.print_task_forest(default_tasks)

        # Print the rest of the tasks
        for cat in sorted(by_category):
            self.print_category(cat)
            self.print_task_forest(by_category[cat])
