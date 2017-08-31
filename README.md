# To Do

This is a simple Python 3 script that serves as a command line to-do list.
It is custom built to my preferences and may change drastically over time.

## Setup

1. Install Python requirements `pip install -r requirements.txt`
2. make an alias in your `.bashrc`:
   `alias todo='/path/to/todo.py'`

## Usage

### Adding Tasks

To add one or more tasks, use the `todo add` subcommand:

```
$ todo add "Do laundry"
Added task T1 - Do laundry

$ todo add "Do dishes" "Buy groceries"
Added task T2 - Do dishes
Added task T3 - Buy groceries
```

### List Tasks

To list tasks, use the `todo list` command. Checked off tasks will
have an X in the brackets.

```
$ todo list
- [ ] T1 - Do laundry
- [x] T2 - Do dishes
- [ ] T3 - Buy groceries
```

### Complete Tasks

To check off a task, use the `todo done` command.

```
$ todo done T1
Checked off task T1 - Do laundry

$ todo done T2 T3
Checked off task T2 - Do dishes
Checked off task T3 - Buy groceries

# uncheck a task with -u/--uncheck
$ todo done -u T2
Unchecked task T2 - do dishes
```
