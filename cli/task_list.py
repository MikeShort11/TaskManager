import json
import task

class TaskList:
    def __init__(self):
        """Constructs an object containing a dictionary of task object.
        self.list: dict[task]"""
        pass

    def add_task(self, name):
        """Uses the Task class to create a task object and
        adds it to the task_list dictionary.
        Automatically calls _save_tasks."""
        pass

    def delete_task(self, name):
        """Deletes a specified task from the task_list dictionary."""
        pass

    def _load_tasks(self):
        """Loads the list of tasks in the JSON into the dictionary."""
        pass

    def _save_tasks(self):
        """Saves new tasks into the JSON from the dictionary"""
        pass

    def __iter__(self):
        """Yields an iterator of all the objects and their data members."""
        pass

    def __str__(self):
        """Yields a string representation of the TaskList's dictionary"""
        pass
