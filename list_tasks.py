from database import db

class ListTasks: 
    def format_task(self, task):
        check = 'x' if task['completed'] else ' '
        tid = 'T{}'.format(task.eid)
        return "- [{}] {} - {}".format(check, tid, task['name'])

    def bucket_categories(self):
        by_category = {}
        for task in db.all():
            category = task.get('category', None)
            by_category.setdefault(category, []).append(task)
        return by_category

    def __call__(self, args):
        by_category = self.bucket_categories()

        # Print default category tasks first
        default_tasks = by_category.get(None, [])
        if default_tasks:
            for task in default_tasks:
                print(self.format_task(task))
            print()

        # Print the rest of the tasks
        for cat in sorted(by_category):
            if cat is None:
                continue
            print(cat)
            for task in by_category[cat]:
                print(self.format_task(task))
            print()
