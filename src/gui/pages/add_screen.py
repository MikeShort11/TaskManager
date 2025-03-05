from kivy.app import App, Builder
#layout imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
#widget layouts
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


from kivy.config import Config
Config.set('graphics', 'width', '395')
Config.set('graphics', 'height', '465')

from kivy.uix.textinput import TextInput

text_field_headings = ["Title", "Category", "Date", "Time", "Description"] #names of text fields


class TopLabel(BoxLayout):
    """the Label at the top of the page"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_label = Label(text="New Task", font_size = (30))
        self.add_widget(self.top_label)

class TaskFields(FloatLayout):
    """The composition of text fields and their titles"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.size = (360, 300)
        y_pos = 150

        for i in text_field_headings:
            if i == "Description":
                label = Label(text=i, pos=(-141, y_pos))
            elif i == "Category":
                label = Label(text=i, pos=(-149, y_pos))
            else:
                label = Label(text=i, pos=(-164, y_pos))
            y_pos -= 33
            if i == "Description":
                text_input = TextInput(pos=(18, y_pos + 185), size=(220, 60), size_hint=(None, None))
            else:
                text_input = TextInput(pos=(18, y_pos + 230), multiline=False, size=(220, 23), size_hint=(None, None), font_size=10)
            y_pos -= 30
            self.add_widget(label)
            self.add_widget(text_input)


class MainApp(App):
    """The main add_screen window"""
    def build(self):
        root = FloatLayout()

        top_label_widget = TopLabel(pos=(-115, 200))
        root.add_widget(top_label_widget)

        task_field_widget = TaskFields()
        root.add_widget(task_field_widget)

        accept_button = Button(pos=(297, 135), size=(40,40), size_hint=(None, None), text="Accept")
        discard_button = Button(pos=(297, 65), size=(40, 40), size_hint=(None, None), text="Discard")
        root.add_widget(accept_button)
        root.add_widget(discard_button)

        return root

if __name__ == '__main__':
    MainApp().run()
