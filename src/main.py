from kivy.app import App
from gui.screens.main_screen import MainScreen
from gui.utils.task_list import TaskList

class TaskManagerApp(App):
    def build(self):
        task_list = TaskList('gui/tasks.json')
        return MainScreen(task_list)

if __name__ == "__main__":
    TaskManagerApp().run()