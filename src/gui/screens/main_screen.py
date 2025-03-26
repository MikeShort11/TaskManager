from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from .task_form_screen import TaskFormModal
from ..utils.task import Task

class TaskItem(BoxLayout):
    def __init__(self, task, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        #make the top half of the layout
        top_half = BoxLayout(orientation='horizontal', size_hint_y=None, size=(100, 75))
        top_half.add_widget(Label(text=task.title))
        edit_button = Button(text="Edit")
        edit_button.bind(on_press=lambda instance: on_edit(task))
        top_half.add_widget(edit_button)
        delete_button = Button(text="Delete")
        delete_button.bind(on_press=lambda instance: on_delete(task))
        top_half.add_widget(delete_button)
        expand_button = Button(on_press=expand_and_collapse)
        top_half.add_widget(expand_button)

        #------------------------------------------------------
        def expand_and_collapse(instance):
            #get the task holder from the button
            task_item = instance.parent.parent
            #resize the holder to move the other tasks down
            task_item.height=150


            bottom_half = BoxLayout(orientation = 'horizontal', size_hint_y=0.5) #needed for formatting reasons

            #checks if the task is already expanded
            if len(task_item.children) > 1:
                task_item.remove_widget(task_holder.children[0])  # Remove old details
                task_item.size = (100, 75)  # Reset size
                instance.text="expand" #change text

            else:
                #TODO: format the details
                details = str(global_task_manager.list[instance.parent.children[1].text])
                #add new widgets
                bottom_half.add_widget(Label(text=details))
                task_item.add_widget(bottom_half)
                instance.text="collapse" #change text

        #------------------------------------------------------

        self.add_widget(top_half)

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
