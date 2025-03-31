import json
from .task import Task

class JsonManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.file_path, 'r') as f:
                tasks_data = json.load(f)
                result = []
                for task in tasks_data:
                    result.append(Task.from_dict(task))
                return result
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.file_path, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)



class TaskList:
    def __init__(self, json_manager: JsonManager):
        self.json_manager = json_manager
        self.tasks = json_manager.tasks

    def update_json(self):
        self.json_manager.tasks = self.tasks
        self.json_manager.save_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.update_json()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.update_json()

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def sort_tasks(self, key_func):
        self.tasks = sorted(self.tasks, key=key_func)

