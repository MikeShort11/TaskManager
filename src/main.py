from kivy.app import App
from gui.screens.main_screen import MainScreen
from gui.utils.task_list import TaskList, JsonManager
from gui.screens.list_manager_screen import ListMainScreen
from gui.utils.list_list import ListList, ListJsonManager

class TaskManagerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.return_task_list = None

    def build(self):
        file_path = "masterlist.json"
        json_manager = ListJsonManager(file_path)
        master_list = ListList(json_manager)
        return ListMainScreen(master_list)

    def run(self):
        super(TaskManagerApp, self).run()
        return self.return_task_list

    def set_return(self, task_list):
        self.return_task_list = task_list

    def set_return_and_stop(self, task_list):
        """Sets the return task list and stops the current app instance."""
        self.set_return(task_list)
        print("TaskManagerApp: Stopping app instance.")
        self.stop()  # Stop the Kivy application loop

class TaskListApp(App):
    def __init__(self, task_list, **kwargs):
        super().__init__(**kwargs)
        self.task_list = task_list

    def build(self):
        return MainScreen(self.task_list)

if __name__ == "__main__":
    running = True
    while running:
        task_list = TaskManagerApp().run()
        if task_list != None:
            TaskListApp(task_list).run()
        else:
            running = False

