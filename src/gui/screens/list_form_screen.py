from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ..utils.task_list import TaskList

class ListFormModal(ModalView):
    def __init__(self, on_save=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        self.input = None

        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, pos_hint=(None, None))
        button_layout=BoxLayout(size_hint_y=None, height=80)

        layout.add_widget(Label(text="NEW TITLE:", size_hint_y=None, height=100))

        text_input = TextInput(multiline=False, size_hint_y=None, height=80)
        layout.add_widget(text_input)

        self.input = text_input

        save_button = Button(text="Save", size_hint_y=None, height=80)
        save_button.bind(on_press=self.save)
        button_layout.add_widget(save_button)

        cancel_button = Button(text="Cancel", size_hint_y=None, height=80)
        cancel_button.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)
        self.on_save = on_save

    def save(self, instance):
        new_title = self.input.text
        print("Return title is:" + new_title)
        if self.on_save:
            self.on_save(new_title)
        self.dismiss()
