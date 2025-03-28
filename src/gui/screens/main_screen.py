from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from .task_form_screen import TaskFormModal
from ..utils.task import Task
import functools

def compare_by_category(task_one: Task, task_two: Task):
    if int(task_one.category) < int(task_two.category):
        return -1
    elif int(task_one.category) > int(task_two.category):
        return 1
    else:
        return 0

class TaskItem(BoxLayout):
    def __init__(self, task, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        #store the task for later referance
        self.task = task
        self.on_delete = on_delete
        self.on_edit = on_edit

        #make the top half of the layout
        top_half = BoxLayout(orientation='horizontal', size_hint_y=None, size=(100, 75))
        top_half.add_widget(Label(text=task.title))
        expand_button = Button(on_press=self.expand_and_collapse, text='expand')
        top_half.add_widget(expand_button)
        self.add_widget(top_half)

    def expand_and_collapse(self, instance):
        #get the task holder from the button
        task_item = instance.parent.parent
        #resize the holder to move the other tasks down
        task_item.height=200
        #get the task info for the description
        task = task_item.task

        text = f"""
        Description: {task.description}
        Date: {task.date}
        Time: {task.time}
        Catergory: {task.category}"""

        bottom_half = BoxLayout(orientation = 'horizontal', size_hint_y=0.5)

        #checks if the task is already expanded
        if len(task_item.children) > 1:
            task_item.remove_widget(task_item.children[0])  # Remove old details
            task_item.size = (100, 75)  # Reset size
            instance.text="expand" #change text
        #TODO: add some logic to put newlines into description
        else:
            #add text and buttons to expanded info
            bottom_half.add_widget(Label(text=text, halign='left', size_hint_x=None, size=(500, 100)))
            #add edit button to expanded info
            edit_button = Button(text="Edit", background_color='green')
            edit_button.bind(on_press=lambda instance: self.on_edit(task))
            bottom_half.add_widget(edit_button)
            #add the delete button the the new menu
            delete_button = Button(text="Delete", background_color='red')
            delete_button.bind(on_press=lambda instance: self.on_delete(task))
            bottom_half.add_widget(delete_button)
            #add the expanded section and change button text
            task_item.add_widget(bottom_half)
            instance.text="collapse" #change text

class MainScreen(BoxLayout):
    def __init__(self, task_list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.task_list = task_list

        # Task list display
        self.task_display = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_display.bind(minimum_height=self.task_display.setter('height'))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.task_display)
        self.add_widget(scroll_view)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50)
        add_button = Button(text="Add Task")
        add_button.bind(on_press=self.add_task)
        button_layout.add_widget(add_button)
        sort_button = Button(text="Sort")
        sort_button.bind(on_press=self.sort_tasks_button)
        button_layout.add_widget(sort_button)
        self.add_widget(button_layout)

        # Populate task list
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_display.clear_widgets()
        for task in self.task_list.tasks:
            task_item = TaskItem(
                                 task,
                                 on_edit=self.edit_task,
                                 on_delete=self.delete_task,
                                 size_hint_y=None,
                                 size=(100,75)
                                 )
            self.task_display.add_widget(task_item)

    def add_task(self, instance):
        form = TaskFormModal(on_save=self.save_new_task)
        form.open()

    def edit_task(self, task):
        form = TaskFormModal(task, on_save=self.save_edited_task)
        form.open()

    def delete_task(self, task):
        self.task_list.delete_task(task.title)
        self.refresh_task_list()

    def save_new_task(self, task_data):
        new_task = Task(**task_data)
        self.task_list.add_task(new_task)
        self.refresh_task_list()

    def save_edited_task(self, task_data):
        title = task_data['title']
        existing_task = self.task_list.get_task(title)
        if existing_task:
            for key, value in task_data.items():
                setattr(existing_task, key, value)
            self.task_list.update_json()
            self.refresh_task_list()

    def sort_tasks_button(self, instance):
        key = functools.cmp_to_key(compare_by_category)
        self.task_list.sort_tasks(key)
        self.refresh_task_list()
