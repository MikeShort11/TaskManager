from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from .task_form_screen import TaskFormModal
from ..utils.task import Task

class TaskItem(BoxLayout):
    def __init__(self, task, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.add_widget(Label(text=task.title))
        edit_button = Button(text="Edit")
        edit_button.bind(on_press=lambda instance: on_edit(task))
        self.add_widget(edit_button)
        delete_button = Button(text="Delete")
        delete_button.bind(on_press=lambda instance: on_delete(task))
        self.add_widget(delete_button)

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
            self.task_list.save_tasks()
            self.refresh_task_list()