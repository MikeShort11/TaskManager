from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ..utils.task_list import TaskList

class AIFormModal(ModalView):
    def __init__(self, on_save=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        self.input = None

        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=400, pos_hint=(None, None))
        button_layout = BoxLayout(size_hint_y=None, height=80)
        self.inputs = {}

        layout.add_widget(Label(text="What do you want to do?", size_hint_y=None, height=100))

        prompt_text_input = TextInput(multiline=True, size_hint_y=None, height=200)
        layout.add_widget(prompt_text_input)
        self.inputs['Prompt'] = prompt_text_input

        title_text_input = TextInput(multiline=False, size_hint_y=None, height=40)
        title_text_input.text = "Title of New List"
        layout.add_widget((title_text_input))
        self.inputs['Title'] = title_text_input





        save_button = Button(text="Save")
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)

        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        self.on_save = on_save

    def save(self, instance):
        ai_data = {field: self.inputs[field].text for field in self.inputs}
        if self.on_save:
            self.on_save(ai_data)
        self.dismiss()
