import json
from task import Task  # Relative import since task.py is in the same directory

class TaskList:
    def __init__(self, json_name=None):
        """Constructs an object containing a dictionary of task objects.
        If json_name is provided, loads tasks from it; otherwise, starts with an empty list."""
        # Initialize attributes regardless of json_name
        self.list = {}  # Dictionary to hold tasks
        self.size = 0   # Size of the task list
        self.json = None  # Will store the JSON file path if provided

        if json_name is not None:
            try:
                assert isinstance(json_name, str)  # Check input type
                assert json_name.endswith(".json")  # Check file extension
                self.json = json_name  # Store the file path
                self._load_tasks(json_name)  # Load tasks from file
                self._get_size()  # Update size after loading
            except AssertionError as e:
                if "str" in str(e):
                    raise TypeError("json_name must be a string")
                raise AttributeError("Incorrect extension. Must be '.json'.")
            except FileNotFoundError:
                # If file doesn't exist, start with empty list and create it later
                print(f"Warning: {json_name} not found. Starting with an empty task list.")
                self.json = json_name  # Still store the path for future saves

    def add_task(self, title):
        """Adds a task to the list and saves if using a JSON file."""
        if title in self.list:
            return f"'{title}' is taken, try another name."
        prev_size = self.size
        self.list[title] = Task(title)
        self._get_size()
        if self.json and self.size != prev_size:
            self._save_tasks(self.json)
        return f"{title} task added successfully."

    def delete_task(self, title):
        """Deletes a task from the list and saves if using a JSON file."""
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
        """Loads tasks from the JSON file into the dictionary."""
        with open(json_name) as file:
            data = json.load(file)
            self.list = {task_data['title']: Task.from_dict(task_data) for task_data in data}

    def _save_tasks(self, json_name):
        """Saves the current tasks to the JSON file."""
        with open(json_name, 'w') as file:
            json.dump([task.to_dict() for task in self.list.values()], file, indent=4)
        # No need to call _load_tasks here; self.list is already up-to-date

    def __iter__(self):
        """Yields an iterator of all task titles."""
        for key in self.list:
            yield key

    def __str__(self):
        """Returns a string representation of the TaskList."""
        if not self.list:
            return "No tasks found in this list."
        return ", ".join(self.list.keys())