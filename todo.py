#!/usr/bin/env python
import argparse
from database import db
from tasks import Task
from add_tasks import AddTasks
from edit_tasks import EditTasks
from done_tasks import DoneTasks
from list_tasks import ListTasks
from delete_tasks import DeleteTasks
from make_subtasks import MakeSubtasks

def task_id(arg):
    if arg[0].upper() != 'T':
        raise argparse.ArgumentTypeError(arg + ": task IDs must begin with T")
    
    try:
        eid = int(arg[1:])
    except ValueError:
        raise argparse.ArgumentTypeError(arg + ": Task ID # must be an int")

    task = db.get(eid=eid)
    if task:
        return Task(task)
    else:
        raise argparse.ArgumentTypeError(arg + ": Task does not exist")

def category(arg):
    cat_name = arg.upper()
    if cat_name == 'NONE':
        return None
    else:
        return cat_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('task_name', nargs='+', 
        help='One or more task names to add to the database')
    add_parser.add_argument('-c', '--category', type=category,
        help='Set a category for the task')
    add_parser.set_defaults(func=AddTasks())

    subtask_parser = subparsers.add_parser('subtask')
    subtask_parser.add_argument('parent', type=task_id,
        help='ID of the parent task.')
    subtask_parser.add_argument('task_name', nargs='+',
        help='One or more task names to add as subtasks') 
    subtask_parser.set_defaults(func=MakeSubtasks())

    done_parser = subparsers.add_parser('done')
    done_parser.add_argument('tasks', nargs='+', type=task_id,
        help='One or more task/subtask IDs')
    done_parser.add_argument('-u', '--uncheck', action='store_true',
        help='If specified, UNcheck tasks')
    done_parser.set_defaults(func=DoneTasks())

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('tasks', nargs='+', type=task_id,
        help='One or more task/subtask IDs')
    delete_parser.set_defaults(func=DeleteTasks())
    
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-c', '--category', nargs='+', type=category,
        help=(
            'Only list tasks of the given categories.'
            'Use "none" to specify no category'))
    list_parser.add_argument('-a', '--all', 
        dest='show_all', action='store_true',
        help='Show all tasks (including completed ones')
    list_parser.set_defaults(func=ListTasks())

    edit_parser = subparsers.add_parser('edit')
    edit_parser.add_argument('-c', '--category', type=category,
        help='set a new category')
    edit_parser.add_argument('-n', '--name',
        help='set all specified tasks to have this name')
    edit_parser.add_argument('tasks', nargs='+', type=task_id,
        help='One or more task IDs to edit. All tasks get the same settings')
    edit_parser.set_defaults(func=EditTasks())

    args = parser.parse_args()
    args.func(args)
    '''
    try:
        args.func(args)
    except AttributeError as e:
        print(e)
        parser.print_help()
    '''
