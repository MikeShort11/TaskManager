from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ..utils.task import Task

class TaskFormModal(ModalView):
    def __init__(self, task=None, on_save=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False

        layout = GridLayout(cols=2)
        self.inputs = {}

        fields = ['title', 'date', 'time', 'description', 'priority']
        for field in fields:
            layout.add_widget(Label(text=field.capitalize() + ':'))
            if field == 'description':
                text_input = TextInput(multiline=True)
            else:
                text_input = TextInput(multiline=False)
            if task:
                text_input.text = getattr(task, field)
            self.inputs[field] = text_input
            layout.add_widget(text_input)

        save_button = Button(text="Save")
        save_button.bind(on_press=self.save)
        layout.add_widget(save_button)

        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        layout.add_widget(cancel_button)

        self.add_widget(layout)
        self.on_save = on_save

    def save(self, instance):
        task_data = {field: self.inputs[field].text for field in self.inputs}
        if self.on_save:
            self.on_save(task_data)
        self.dismiss()