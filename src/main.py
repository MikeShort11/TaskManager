from kivy.app import App
from kivy.core.window import Window
from gui.screens.main_screen import MainScreen
from gui.utils.task_list import TaskList, JsonManager
from gui.screens.list_manager_screen import ListMainScreen
from gui.utils.list_list import ListList, ListJsonManager
from kivy.config import Config

from kivymd.app import MDApp

Config.set('graphics', 'width', '790')
Config.set('graphics', 'height', '930')
Config.set('graphics', 'resizable', '0')
Window.size = (770, 930)
Window.minimum_width = 770
Window.minimum_height = 930
Window.resizable = False

class TaskManagerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.return_task_list = None

    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Black"

        file_path = "gui/masterlist.json"
        json_manager = ListJsonManager(file_path)
        master_list = ListList(json_manager)
        return ListMainScreen(master_list)

    def run(self):
        super(TaskManagerApp, self).run()
        return self.return_task_list

    def set_return(self, task_list):
        self.return_task_list = task_list

class TaskListApp(MDApp):
    def __init__(self, task_list, **kwargs):
        super().__init__(**kwargs)
        self.task_list = task_list

    def build(self):
        Window.size = (770, 930)
        return MainScreen(self.task_list)

if __name__ == "__main__":
    running = True
    while running:
        task_list = TaskManagerApp().run()
        if task_list != None:
            TaskListApp(task_list).run()
        else:
            running = False

