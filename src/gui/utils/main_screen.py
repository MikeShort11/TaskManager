from pathlib import Path
import json
from src.gui.utils.task_list import TaskList
from kivy.app import App
#layout imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#widget layouts
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class JsonLoader:
    """
    A class to load JSON data from a file in the 'utils' directory,
    located one level above the module containing this class.
    """

    def __init__(self):
        """Initialize the JsonLoader by determining the path to the JSON file."""
        self.json_file_path = self._get_json_file_path()

    @staticmethod
    def _get_json_file_path():
        """
        Private method to locate the first JSON file in the 'utils' directory.

        Returns:
            Path: The path to the first JSON file.

        Raises:
            FileNotFoundError: If no JSON files are found in the 'utils' directory.
        """
        # Get the absolute path of the directory containing this module
        module_dir = Path(__file__).resolve().parent

        # Navigate one level up and into the 'utils' directory
        utils_dir = module_dir.parent / 'utils'

        # Find all files with a '.json' extension in the 'utils' directory
        json_files = list(utils_dir.glob('*.json'))

        if json_files:
            # Return the first JSON file found
            return json_files[0].name
        else:
            raise FileNotFoundError("No JSON files found in the 'utils' directory")

    def load_json(self):
        """
        Load and return the JSON data from the file as a Python object.

        Returns:
            dict/list: The parsed JSON data (type depends on the JSON content).

        Raises:
            json.JSONDecodeError: If the file contains invalid JSON.
            FileNotFoundError: If the file cannot be found at runtime.
            IOError: If there’s an issue reading the file.
        """
        with self.json_file_path.open('r') as f:
            return json.load(f)

JSON_LOADER = JsonLoader()  # Returns a str
JSON_NAME = TaskList(JSON_LOADER.json_file_path)

class TopLabel(BoxLayout):
    """the Label at the top of the page"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y=0.1 #size_hint allows for flexibility
        self.top_label = Label(text="Super Cool Task Manager")
        self.add_btn = Button(text='add_task', size_hint_x=0.1)
        self.add_btn.bind(on_press=add_task)
        self.add_widget(self.top_label)
        self.add_widget(self.add_btn)


class ListDisplay(ScrollView):
    #the scroll view holds the layouts so they can expand past the screen and be scrolled
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #the list of tasks holds the task objects that will be displayed
        list_of_tasks = GridLayout(cols=1, size_hint_y=None)
        list_of_tasks.bind(minimum_height=list_of_tasks.setter('height'))  # Ensure list_of tasks resizes with number of tasks

        #loop through the data to get the labels for the tasks  TODO: replace temp_list
        for i in JSON_NAME:
            task_holder = BoxLayout(orientation='vertical', size_hint_y=None, size=(100, 75)) #also where the additional details will go
            task = BoxLayout(orientation='horizontal', size_hint_y=None, size=(100, 75)) #holds the name of the task and the button to expand
            lbl = Label(text=i) #the text for the task
            btn = Button(text="expand", size_hint_x=0.1) #the button to expand the task
            #add the items to the larger layout
            btn.bind(on_press=expand_and_collapse)
            task.add_widget(lbl)
            task.add_widget(btn)
            task_holder.add_widget(task)
            list_of_tasks.add_widget(task_holder)

        self.add_widget(list_of_tasks)

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.return_value = "none"

    def build(self):
        root = BoxLayout(orientation="vertical")

        top_label_widget = TopLabel()
        list_display_widget = ListDisplay()

        root.add_widget(top_label_widget)
        root.add_widget(list_display_widget)

        return root

    def run(self):
        super(MainApp, self).run()
        return self.return_value

    def set_return(self, input:str):
        self.return_value = input



def expand_and_collapse(instance):
    #get the task holder from the button
    task_holder = instance.parent.parent
    #resize the holder to move the other tasks down
    task_holder.height=150
    edit_btn = Button(text='edit', size_hint_x=0.1)
    delete_btn = Button(text='delete', size_hint_x=0.1)

    edit_btn.bind(on_press=edit_task)
    delete_btn.bind(on_press=delete_task)

    detail_holder = BoxLayout(orientation = 'horizontal', size_hint_y=0.5) #needed for formatting reasons

    #checks if the task is already expanded
    if len(task_holder.children) > 1:
        task_holder.remove_widget(task_holder.children[0])  # Remove old details
        task_holder.size = (100, 75)  # Reset size
        instance.text="expand" #change text

    else:
        #TODO: format the details
        details = str(JSON_NAME.list[instance.parent.children[1].text])
        #add new widgets
        detail_holder.add_widget(Label(text=details))
        detail_holder.add_widget(edit_btn)
        detail_holder.add_widget(delete_btn)
        task_holder.add_widget(detail_holder)
        instance.text="collapse" #change text

def add_task(instance):
    task = instance.parent.parent.children[1].children[1].text
    App.get_running_app().set_return(("add", task))
    App.get_running_app().stop()

def edit_task(instance):
    task = instance.parent.parent.children[1].children[1].text
    App.get_running_app().set_return(("edit", task))
    App.get_running_app().stop()

def delete_task(instance):
    task = instance.parent.parent.children[1].children[1].text
    App.get_running_app().set_return(("delete", task))
    App.get_running_app().stop()

if __name__ == '__main__':
    MainApp().run()

