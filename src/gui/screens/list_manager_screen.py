from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from .list_form_screen import ListFormModal
from .main_screen import MainScreen
from ..utils.task_list import TaskList, JsonManager
from ..utils.json_generator import JsonGenerator
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDIconButton
from kivymd.uix.screen import MDScreen




class ListItem(BoxLayout):
    def __init__(self, list, on_edit, on_delete, on_open, **kwargs):
        super().__init__(**kwargs)
        #store the list for later reference
        self.list = list
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_open = on_open

        self.pos = (0, 0)

        #make the top half of the layout
        self.top_half = FloatLayout(size_hint=(None, None), size=(790, 80))
        open_button = Button(on_press=lambda instance: on_open(list), pos=(0, 0), size_hint=(None, None),
                             size=(790, 80))
        open_button.background_color = (0.5, 0.5, 0.5, 1)
        list_title = Label(text=list.title, size_hint=(None, None), pos=(0, -10), font_size="30sp")

        expand_button = MDIconButton(on_press=self.expand_and_collapse, icon="arrow-right-drop-circle", theme_font_size="Custom", font_size="44sp", pos=(710, 20), size_hint=(None, None),
                               size=(100, 100), style="tonal", theme_bg_color="Custom", md_bg_color="black", theme_icon_color="Custom",
                                     icon_color="white")




        self.top_half.add_widget(open_button)
        self.top_half.add_widget(expand_button)
        self.top_half.add_widget(list_title)
        self.add_widget(self.top_half)

        # self.add_widget(expand_button)
        # self.add_widget(list_title)
        # self.add_widget(open_button)





    def expand_and_collapse(self, instance):
        #get the task holder from the button
        list_item = instance.parent
        #resize the holder to move the other tasks down
        list_item.height=100
        #get the task info for the description
        list = list_item.list





        bottom_half = FloatLayout(size=(100, 400))

        #checks if the task is already expanded
        if len(list_item.children) > 1:
            list_item.remove_widget(list_item.children[0]) # Remove old details
            list_item.size = (100, 75)  # Reset size
            instance.icon="arrow-right-drop-circle" #change text

        else:
            text_input = TextInput(text="New List Title", halign='left', size_hint=(None, None), size=(500, 50))
            bottom_half.add_widget(text_input)
            #add edit button to expanded info
            edit_button = Button(text="Save", background_color='green', size_hint=(None, None), size=(40, 40),
                                 pos=(0,0))
            edit_button.bind(on_press=lambda instance: self.on_edit(list, text_input.text))
            bottom_half.add_widget(edit_button)
            #add the delete button the the new menu
            delete_button = Button(text="Delete", background_color='red', size_hint=(None, None), size=(40, 40),
                                   pos=(95,0))
            delete_button.bind(on_press=lambda instance: self.on_delete(list))
            bottom_half.add_widget(delete_button)
            #add the expanded section and change button text
            list_item.add_widget(bottom_half)
            instance.icon="arrow-down-drop-circle" #change text



class ListMainScreen(FloatLayout):
    def __init__(self, list_list, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'vertical'
        self.size = (790, 930)
        self.master_list = list_list



        # List display
        self.list_display = BoxLayout(orientation='vertical', size_hint=(None, None), size=(790, 930))
        self.list_display.bind(minimum_height=self.list_display.setter('height'))
        scroll_view = ScrollView(size_hint=(None, None), size=(790, 930))
        scroll_view.add_widget(self.list_display)
        self.add_widget(scroll_view)

        # Buttons
        button_layout = FloatLayout(size_hint=(None, None), size=(790, 930))
        add_button = MDIconButton(text="NEW LIST", icon="plus", pos=(670, 55))
        add_button.bind(on_press=self.add_list)
        button_layout.add_widget(add_button)
        self.add_widget(button_layout)

        # Populate task list
        self.refresh_list()
        # print(self.list_display.children[3].list.title)


    def refresh_list(self):
        print(f"Refreshing list... Current list count: {len(self.master_list.lists)}")
        self.list_display.clear_widgets()
        for list in self.master_list.lists:
            print(f"Adding ListItem for: {list.title}")
            list_item = ListItem(
                                 list,
                                 on_edit=self.edit_list,
                                 on_delete=self.delete_list,
                                 on_open=self.open_list,
                                 size_hint=(None, None),
                                 size=(790, 80),



                                 )

            self.list_display.add_widget(list_item)



    def add_list(self, instance):
        form = ListFormModal(on_save=self.save_new_list)
        form.open()

    def edit_list(self, list, input):
        new_title = input
        existing_list = self.master_list.get_list(list.title)
        if existing_list:
            existing_list.title = new_title
            self.master_list.update_json()
        self.refresh_list()

    def delete_list(self, list):
        self.master_list.delete_list(list.title)
        self.refresh_list()

    def save_new_list(self, new_title):
        new_file_path = JsonGenerator.new_json(self, title=new_title)
        new_json_manager = JsonManager(new_file_path)
        new_list = TaskList(new_title, new_json_manager)
        self.master_list.add_list(new_list)
        self.refresh_list()

    def open_list(self, list):
        App.get_running_app().set_return(list)
        App.get_running_app().stop()


