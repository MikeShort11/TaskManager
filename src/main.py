from kivy.app import App
from gui.screens.main_screen import MainScreen
from gui.utils.task_list import TaskList, JsonManager
from gui.screens.list_manager_screen import ListMainScreen
from gui.utils.list_list import ListList, ListJsonManager

class TaskManagerApp(App):
    def build(self):
        file_path = "gui/masterlist.json"
        json_manager = ListJsonManager(file_path)
        master_list = ListList(json_manager)
        return ListMainScreen(master_list)

if __name__ == "__main__":
    TaskManagerApp().run()