from database import db
from tasks import Task

class EditTasks: 
    def make_single_props(self, args):
        """
        Reformat non-recursive properties from the arguments into
        a dict for tinydb.
        - name
        """
        props = {}
        
        if args.name:
            props['name'] = args.name

        return props

    def make_recursive_props(self, args):
        """
        Reformat non-recursive properties from the arguments into
        a dict for tinydb.
        - category
        """
        props = {}
        
        if args.category:
            props['category'] = args.category

        print(props)
        return props

    def update_single_properties(self, tasks, props):
        """
        Update non-recursive properties.
        """
        eids = [t.eid for t in tasks]
        db.update(props, eids=eids)

    def update_recursive_properties(self, task, props): 
        """
        Propagate recursive properties

        This is done with a pre-order traversal.
        """
        db.update(props, eids=[task.eid])
        for subtask in task.subtasks:
            self.update_recursive_properties(subtask, props)

    def __call__(self, args):
        # Construct the task forest
        tasks = [Task(t) for t in db.all()]
        task_table = Task.build_task_table(tasks)

        # Handle properties that do not propagate recursively
        single_props = self.make_single_props(args)
        self.update_single_properties(args.tasks, single_props)

        # Handle recursive properties
        recursive_props = self.make_recursive_props(args)
        for task in args.tasks:
            table_task = task_table.get(task.eid, None)
            if table_task:
                self.update_recursive_properties(task, recursive_props)

        # Report results
        eids = [t.eid for t in args.tasks]
        for eid in eids:
            task = Task.from_eid(eid)
            print("Updated task {}".format(task))
