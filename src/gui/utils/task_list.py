import json
from task import Task

class TaskList:
    def __init__(self, json_name = None):
        """Constructs an object containing a dictionary of task object.
        Checks for the json title type, json extension, and its existence."""
        try:
            assert isinstance(json_name, str) or json_name is None  # Check input type
        except AssertionError:
            raise TypeError("Not a String or NoneType.")
        if json_name is not None:
            try:
                assert json_name.endswith(".json")  # Check file extension
            except AssertionError:
                raise AttributeError("Incorrect extension. Must be '.json'.")
            try:
                self._load_tasks(json_name)
            except FileNotFoundError as err:
                raise FileNotFoundError(err)
               

    def add_task(self, title):
        """Uses the Task class to create a task object and
        adds it to the task_list dictionary.
        Automatically calls _save_tasks if needed."""
        if title in self.list:
            return f"'{title}' is taken, try another name."
        prev_size = self.size
        self.list[title] = Task(title)
        self._get_size()
        if self.json and self.size != prev_size:
            self._save_tasks(self.json)
        return f"{title} task added successfully."


    def delete_task(self, title):
        """Deletes a specified task from the task_list dictionary.
        Automatically calls _save_tasks if needed."""
        try:
            prev_size = self.size
            del self.list[title]
            self._get_size()
            if self.json and self.size != prev_size:
                self._save_tasks(self.json)
        except KeyError:
            return "Key not found!"
        else:
            return f"{title} deleted."

    def _get_size(self):
        """Updates the current size of the list dictionary."""
        self.size = len(self.list)

    def _load_tasks(self, json_name):
        """Loads the list of tasks in the JSON into the dictionary."""
        with open(json_name) as file:  # 'read' mode is default in open
            data = json.load(file)
            self.list = {task_data['title']: Task.from_dict(task_data) for task_data in data}

    def _save_tasks(self, json_name):
        """Saves new tasks into the JSON from the dictionary"""
        file_path = json_name
        with open(file_path, 'w') as file:
            json.dump([task.to_dict() for task in self.list.values()], file, indent=4)
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
        return_string = return_string[:-2]  # Gets rid of last item's ", "

        if return_string == "":
            return "No tasks found in this list."

        return return_string
