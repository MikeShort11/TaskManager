from kivy.app import App
from gui.screens.main_screen import MainScreen
from gui.utils.task_list import TaskList, JsonManager

class TaskManagerApp(App):
    def build(self):
        data = JsonManager('gui/tasks.json')
        task_list = TaskList(data)
        return MainScreen(task_list)

if __name__ == "__main__":
    TaskManagerApp().run()