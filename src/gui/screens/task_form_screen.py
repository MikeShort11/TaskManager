from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from ..utils.task import Task
from kivy.config import Config
from kivymd.uix.label import MDLabel

Config.set('graphics', 'width', '395')
Config.set('graphics', 'height', '465')



class TaskFormModal(ModalView):
    def __init__(self, task=None, on_save=None, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (592, 698)

        layout = FloatLayout()
        self.inputs = {}
        if task:
            title = MDLabel(text="Edit Task", font_style="Display", pos=(130, 385), text_color="white")
        else:
            title = MDLabel(text="New Task", font_style="Display", pos=(125, 390), text_color="white")
        layout.add_widget(title)



        y_pos = 320

        fields = ['title', 'time', 'priority', 'date', 'description']

        for field in fields:
            if field == 'description':
                layout.add_widget(Label(text=field.capitalize() + ':', pos=(-130, y_pos)))
            elif field == 'priority':
                layout.add_widget(Label(text=field.capitalize() + ':', pos=(-145, y_pos)))
            else:
                layout.add_widget(Label(text=field.capitalize() + ':', pos=(-145, y_pos)))

            y_pos -= 33

            if field == 'description':
                text_input = TextInput(multiline=True, pos=(250, y_pos + 185), size=(220, 60), size_hint=(None, None))
                if task:
                    text_input.text = getattr(task, field)
                self.inputs[field] = text_input
                layout.add_widget(text_input)



            elif field == 'date':

               months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
               days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                       15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                       27, 28, 29, 30, 31]
               years = [25, 26, 27]

               month_dropdown = DropDown()
               for i in range(12):
                   month_button = Button(text=str(months[i]))
                   month_button.bind(on_release=lambda btn: month_dropdown.select(month_button.text))
                   month_dropdown.add_widget(month_button)
               month_main_button = Button(text="Month", size_hint=(None, None),
                                          size=(80, 40))
               # month_main_button.pos_hint = {'x': 1, 'y': 2}
               month_main_button.bind(on_release=month_dropdown.open)
               month_dropdown.bind(on_select=lambda instance, x: setattr(month_main_button, 'text', x))
               layout.add_widget(month_main_button)

               day_dropdown = DropDown()
               for i in range(31):
                   day_button = Button(text=str(days[i]))
                   day_button.bind(on_release=lambda btn: day_dropdown.select(day_button.text))
                   day_dropdown.add_widget(day_button)
               day_main_button = Button(text="Day", size_hint=(None, None), size=(20, 20))
               # day_main_button.pos_hint = {'x': 2, 'y': 2}
               day_main_button.bind(on_release=day_dropdown.open)
               day_dropdown.bind(on_select=lambda instance, x: setattr(day_main_button, 'text', x))
               layout.add_widget(day_main_button)

               year_dropdown = DropDown()
               for i in range(3):
                   year_button = Button(text=str(years[i]))
                   year_button.bind(on_release=lambda btn: day_dropdown.select(year_button.text))
                   year_dropdown.add_widget(year_button)
               year_main_button = Button(text="Year", size_hint=(None, None), size=(20, 20))
               # year_main_button.pos_hint = {'x': 3, 'y': 2}
               year_main_button.bind(on_release=year_dropdown.open)
               year_dropdown.bind(on_select=lambda instance, x: setattr(year_main_button, 'text', x))
               layout.add_widget(year_main_button)


            else:
                text_input = TextInput(multiline=False, pos=(18, y_pos + 230),size=(220, 23), size_hint=(None, None), font_size=10)
                if task:
                    text_input.text = getattr(task, field)
                self.inputs[field] = text_input
                layout.add_widget(text_input)

        save_button = Button(text="Save", pos=(520, 165), size=(50, 50), size_hint=(None, None))
        save_button.bind(on_press=self.save)
        layout.add_widget(save_button)

        cancel_button = Button(text="Cancel", pos=(520, 95), size=(50, 50), size_hint=(None, None))
        cancel_button.bind(on_press=self.dismiss)
        layout.add_widget(cancel_button)

        self.add_widget(layout)
        self.on_save = on_save

    def save(self, instance):
        task_data = {field: self.inputs[field].text for field in self.inputs}
        if self.on_save:
            self.on_save(task_data)
        self.dismiss()

    def generate_date_field(self):
        date_layout = FloatLayout(pos_hint=0)
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                27, 28, 29, 30, 31]
        years = [25, 26, 27]

        month_dropdown = DropDown()
        for i in range(12):
            month_button = Button(text=str(months[i]))
            month_button.bind(on_release=lambda btn: month_dropdown.select(month_button.text))
            month_dropdown.add_widget(month_button)
        month_main_button = Button(text="Month", size_hint=(None, None),
                                   size=(80, 40))
        # month_main_button.pos_hint = {'x': 1, 'y': 2}
        month_main_button.bind(on_release=month_dropdown.open)
        month_dropdown.bind(on_select=lambda instance, x: setattr(month_main_button, 'text', x))
        date_layout.add_widget(month_main_button)

        day_dropdown = DropDown()
        for i in range(31):
            day_button = Button(text=str(days[i]))
            day_button.bind(on_release=lambda btn: day_dropdown.select(day_button.text))
            day_dropdown.add_widget(day_button)
        day_main_button = Button(text="Day", size_hint=(None, None), size=(20, 20))
        # day_main_button.pos_hint = {'x': 2, 'y': 2}
        day_main_button.bind(on_release=day_dropdown.open)
        day_dropdown.bind(on_select=lambda instance, x: setattr(day_main_button, 'text', x))
        date_layout.add_widget(day_main_button)

        year_dropdown = DropDown()
        for i in range(3):
            year_button = Button(text=str(years[i]))
            year_button.bind(on_release=lambda btn: day_dropdown.select(year_button.text))
            year_dropdown.add_widget(year_button)
        year_main_button = Button(text="Year", size_hint=(None, None), size=(20, 20))
        # year_main_button.pos_hint = {'x': 3, 'y': 2}
        year_main_button.bind(on_release=year_dropdown.open)
        year_dropdown.bind(on_select=lambda instance, x: setattr(year_main_button, 'text', x))
        date_layout.add_widget(year_main_button)

        return date_layout