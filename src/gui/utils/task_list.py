import json
from .task import Task

class TaskList:
    def __init__(self, file_path):
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

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None