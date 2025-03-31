import json
from .task_list import TaskList


class ListJsonManager:
    def __init__(self, file_path: str):
        self.file_path = 'masterlist.json'
        self.lists = self.load_lists()

    def load_lists(self):
        try:
            with open(self.file_path, 'r') as f:
                tasks_data = json.load(f)
                result = []
                for task in tasks_data:
                    result.append(TaskList.from_dict(task))
                return result
        except FileNotFoundError:
            return []

    def save_lists(self):
        with open(self.file_path, 'w') as f:
            json.dump([list.to_dict() for list in self.lists], f, indent=4)


class ListList:
    def __init__(self, title: str, json_manager: ListJsonManager):
        self.json_manager = json_manager
        self.lists = json_manager.lists

    def update_json(self):
        self.json_manager.lists = self.lists
        self.json_manager.save_lists()

    def add_list(self, list):
        self.lists.append(list)
        self.update_json()

    def delete_list(self, title):
        self.lists = [list for list in self.lists if list.title != title]
        self.update_json()

    def get_list(self, title):
        for list in self.list:
            if list.title == title:
                return list
        return None


