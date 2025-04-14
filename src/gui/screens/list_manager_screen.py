from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from .list_form_screen import ListFormModal
from .main_screen import MainScreen
from ..utils.task_list import TaskList, JsonManager
from ..utils.json_generator import JsonGenerator
from ..utils.AI_caller import AICaller
from .ai_form_screen import AIFormModal

from kivy.app import App


class ListItem(BoxLayout):
    def __init__(self, list, on_edit, on_delete, on_open, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        #store the list for later referance
        self.list = list
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_open = on_open

        #make the top half of the layout
        top_half = BoxLayout(orientation='horizontal', size_hint_y=None, size=(100, 75))
        top_half.add_widget(Label(text=list.title))
        expand_button = Button(on_press=self.expand_and_collapse, text='expand')
        top_half.add_widget(expand_button)
        open_button = Button(on_press=lambda instance: on_open(list), text='open')
        top_half.add_widget(open_button)
        self.add_widget(top_half)

    def expand_and_collapse(self, instance):
        #get the task holder from the button
        list_item = instance.parent.parent
        #resize the holder to move the other tasks down
        list_item.height=200
        #get the task info for the description
        list = list_item.list

        bottom_half = BoxLayout(orientation = 'horizontal', size_hint_y=0.5)

        #checks if the task is already expanded
        if len(list_item.children) > 1:
            list_item.remove_widget(list_item.children[0])  # Remove old details
            list_item.size = (100, 75)  # Reset size
            instance.text="expand" #change text

        else:
            text_input = TextInput(text="New List Title", halign='left', size_hint=(None, None), size=(500, 100))
            bottom_half.add_widget(text_input)
            #add edit button to expanded info
            edit_button = Button(text="Save", background_color='green')
            edit_button.bind(on_press=lambda instance: self.on_edit(list, text_input.text))
            bottom_half.add_widget(edit_button)
            #add the delete button the the new menu
            delete_button = Button(text="Delete", background_color='red')
            delete_button.bind(on_press=lambda instance: self.on_delete(list))
            bottom_half.add_widget(delete_button)
            #add the expanded section and change button text
            list_item.add_widget(bottom_half)
            instance.text="collapse" #change text



class ListMainScreen(BoxLayout):
    def __init__(self, list_list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.master_list = list_list


        # List display
        heading = Label(text="Lists:", font_size="40sp", size_hint_y=None, size_hint_x=.17)
        self.add_widget(heading)
        self.list_display = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_display.bind(minimum_height=self.list_display.setter('height'))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.list_display)
        self.add_widget(scroll_view)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, orientation='horizontal')
        add_button = Button(text="NEW LIST")
        add_button.bind(on_press=self.add_list)

        ai_button = Button(text='AI')
        ai_button.bind(on_press=self._prompt_ai)

        button_layout.add_widget(add_button)
        button_layout.add_widget(ai_button)

        self.add_widget(button_layout)

        # Populate task list
        self.refresh_list()

    def refresh_list(self):
        self.list_display.clear_widgets()
        for list in self.master_list.lists:
            list_item = ListItem(
                                 list,
                                 on_edit=self.edit_list,
                                 on_delete=self.delete_list,
                                 on_open=self.open_list,
                                 size_hint_y=None,
                                 size=(100,75)
                                 )
            self.list_display.add_widget(list_item)

    def _prompt_ai(self, instance):
        form = AIFormModal(on_save=self.save_ai_list)
        form.open()


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

    def save_ai_list(self, ai_data):
        ai_title = ai_data['Title']
        ai_text = AICaller().make_AI_tasklist(ai_data['Prompt'])
        new_file_path = JsonGenerator.string_to_json(self, title=ai_title, content=ai_text)
        new_json_manager = JsonManager(new_file_path)
        new_list = TaskList(ai_title, new_json_manager)
        self.master_list.add_list(new_list)
        self.refresh_list()



    def open_list(self, list):
        App.get_running_app().set_return(list)
        App.get_running_app().stop()



