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

    def write_json(self, file_name):
        file_name = json.dumps(self.list, indent=4)

    def add_task(self, title):
        """Uses the Task class to create a task object and
        adds it to the task_list dictionary.
        Automatically calls _save_tasks if needed."""
        prev_size = self.size
        self.list[title] = task.Task(title)
        self._get_size()
        if self.json and self.size != prev_size:
            self._save_tasks(self.json)

    def delete_task(self, title):
        """Deletes a specified task from the task_list dictionary.
        Automatically calls _save_tasks if needed."""
        try:
            prev_size = self.size
            self.list.pop(title)
            self._get_size()
            if self.json and self.size != prev_size:
                self._save_tasks(self.json)
        except KeyError:
            print("Key not found!")
            return "Key not found!"

    def _get_size(self):
        """Updates the current size of the list dictionary."""
        self.size = len(self.list)

    def _load_tasks(self, json_name):
        """Loads the list of tasks in the JSON into the dictionary."""
        with open(json_name) as file:  # 'read' mode is default in open
            data = json.load(file)
            self.list = data

    def _save_tasks(self, json_name):
        """Saves new tasks into the JSON from the dictionary"""
        file_path = json_name
        with open(file_path, 'w') as file:
            json.dump(self.list, file, indent=4)
        self._load_tasks(json_name)

    def __iter__(self):
        """Yields an iterator of all the objects' titles."""
        for key, task in self.list.items():
            yield key


    def __str__(self):
        """Returns a string representation of the TaskList's dictionary"""
        return_string = ""
        for key, task in self.list.items():
            return_string += key + ", "
        return_string = return_string[:-2]

        if return_string == "":
            return "No tasks found in this list."

        return return_string
