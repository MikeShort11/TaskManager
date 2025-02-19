from task_list import TaskList
import task
from datetime import datetime
import json
import os

def welcome_menu():
    while True:
        print("""Enter a command:
              1. Load Task Manager 
              2. Create Task Manager"""
              )
        selection = input()
        if selection == "1":
            print("Please provide JSON file name")
            json_name = input()
            task_manager_list = TaskList(json_name)
            break
        elif selection == "2":
            task_manager_list = TaskList()
            print("Please name the Task Manager")
            json_name = input()
            json_object = json.dumps(json_name, indent=4)
            task_manager_list.json = json_object
            break
        else:
            print("Please enter 1 or 2")

    return task_manager_list

def view_tasks(task_manager_list):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(task_manager_list)

def add(task_manager_list):
    title = input("New task name? ")
    task_manager_list.add_task(title)

def delete(task_manager_list):
    title = input("Task to delete?")
    task_manager_list.delete_task(title)

def edit(task_manager_list):
    print("task manager list dictonary:\n")
    print(task_manager_list.list)
    edit_task_name = input("Task to edit?")
    new_title = input("New title name?")
    if new_title != "":
        task_manager_list.list[edit_task_name].title = new_title
    new_date = input("New date?")
    if new_date != "":
        task_manager_list.list[edit_task_name].date = new_date
    new_time = input("New time?")
    if new_time != "":
        task_manager_list.list[edit_task_name].time = new_time
    new_description = input("New description?")
    if new_description != "":
        task_manager_list.list[edit_task_name].description = new_description
    new_category = input("New category?")
    if new_category != "":
        task_manager_list.list[edit_task_name].category = new_category
    task_manager_list._save_tasks(task_manager_list.json)


def help_menu():
    print("""Enter a command: 
            add - adds a task to the list
            delete - deletes a task
            edit - edits the task data
            quit - quit the application"""
          )
    command = input("Press enter to exit help menu")
    if command == "":
        return
    else:
        help_menu()


def main(*args, **kwargs):
    task_manager_list = welcome_menu()
    command_dict = {"add": lambda: add(task_manager_list),
                    "delete": lambda: delete(task_manager_list),
                    "edit": lambda: edit(task_manager_list),
                    "quit": lambda: exit(),
                    "help": lambda: help_menu()
                    }
    while True:
        view_tasks(task_manager_list)
        command = input("Enter a command (type 'help' for help): ")
        try:
            command_dict[command]()
        except KeyError:
            print("Command not recognized. Press h for help")


if __name__ == "__main__":
    main()
