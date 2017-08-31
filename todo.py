#!/usr/bin/env python
import argparse
from add_task import AddTask
from list_tasks import ListTasks

def todo(args):
    print(args)

def subtask(args):
    print(args)

def done(args):
    print(args)

def list_tasks(args):
    print(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=todo)
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('task_name', nargs='+', 
        help='One or more task names to add to the database')
    add_parser.add_argument('-c', '--category', 
        help='Set a category for the task')
    add_parser.set_defaults(func=AddTask())

    subtask_parser = subparsers.add_parser('subtask')
    subtask_parser.add_argument('parent_id',
        help='ID of the parent task.')
    subtask_parser.add_argument('task_name', nargs='+',
        help='One or more task names to add as subtasks') 
    subtask_parser.set_defaults(func=subtask)

    done_parser = subparsers.add_parser('done')
    done_parser.add_argument('task_id', nargs='+',
        help='One or more task/subtask IDs')
    done_parser.set_defaults(func=done)
    
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-c', '--category', nargs='+',
        help='Only list tasks of the given categories')
    list_parser.set_defaults(func=ListTasks())

    args = parser.parse_args()
    args.func(args)
