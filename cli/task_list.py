import json
import task

class TaskList:
    def __init__(self, json_name = None):
        """Constructs an object containing a dictionary of task object."""
        self.list: dict = {}
        self.size: int = 0
        self.json: str | None = json_name
        if json_name:
            self._load_tasks(json_name)


    def add_task(self, title):
        """Uses the Task class to create a task object and
        adds it to the task_list dictionary.
        Automatically calls _save_tasks."""
        prev_size = self.size
        self.list[title] = task.Task(title)
        self._get_size()
        if self.json and self.size != prev_size:
            self._save_tasks(self.json)

    def delete_task(self, name):
        """Deletes a specified task from the task_list dictionary."""
        pass

    def _get_size(self):
        self.size = len(self.list)

    def _load_tasks(self, json_name):
        """Loads the list of tasks in the JSON into the dictionary."""
        pass

    def _save_tasks(self, json_name):
        """Saves new tasks into the JSON from the dictionary"""
        pass

    def __iter__(self):
        """Yields an iterator of all the objects and their data members."""
        pass

    def __str__(self):
        """Yields a string representation of the TaskList's dictionary"""
        pass
