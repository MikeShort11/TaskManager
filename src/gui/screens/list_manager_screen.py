from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.metrics import dp

from .list_form_screen import ListFormModal
from ..utils.task_list import TaskList, JsonManager
from ..utils.json_generator import JsonGenerator
from ..utils.AI_caller import AICaller
from .ai_form_screen import AIFormModal

import threading


class ListItem(BoxLayout):
    def __init__(self, list_obj, on_edit, on_delete, on_open, **kwargs):
        super().__init__(orientation='vertical',
                         padding=dp(10),
                         spacing=dp(5),
                         **kwargs) # kwargs pass height
        self.list = list_obj
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_open = on_open

        top_half = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        top_half.add_widget(Label(text=list_obj.title))
        expand_button = Button(on_press=self.expand_and_collapse, text='expand', size_hint_x=0.3)
        top_half.add_widget(expand_button)
        open_button = Button(on_press=lambda instance: self.on_open(self.list), text='open', size_hint_x=0.3)
        top_half.add_widget(open_button)
        self.add_widget(top_half)

        self._collapsed_height = dp(75)
        self._expanded_height = dp(150)

    def expand_and_collapse(self, instance):
        list_item = self

        # Check if the item is currently expanded
        if len(list_item.children) > 1:
            # Collapse - Remove the bottom half and reset height
            list_item.remove_widget(list_item.children[0])
            list_item.height = self._collapsed_height
            instance.text = "Expand"
        else:
            list_item.height = self._expanded_height

            # editing/deleting
            bottom_half = BoxLayout(orientation='horizontal',
                                    padding=dp(5),
                                    spacing=dp(10)) # Space between elements

            # new title
            text_input = TextInput(text=self.list.title,
                                   hint_text="New List Title",
                                   halign='left',
                                   size_hint_x=0.6) # input field spacing
            bottom_half.add_widget(text_input)

            # Standardize button sizes
            edit_button = Button(text="Save Title",
                                 background_color=(0.2, 0.6, 0.2, 1), # green
                                 size_hint=(None, None),
                                 size=(dp(100), dp(40))) # wider for text
            edit_button.bind(on_press=lambda inst: self.on_edit(self.list, text_input.text))
            bottom_half.add_widget(edit_button)

            delete_button = Button(text="Delete List",
                                   background_color=(0.8, 0.2, 0.2, 1), # red
                                   size_hint=(None, None),
                                   size=(dp(100), dp(40)))
            delete_button.bind(on_press=lambda inst: self.on_delete(self.list))
            bottom_half.add_widget(delete_button)

            list_item.add_widget(bottom_half)
            instance.text = "Collapse"



class ListMainScreen(BoxLayout):
    def __init__(self, list_list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.master_list = list_list

        # List display area
        list_area_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))

        heading = Label(text="Lists:", font_size="40sp", size_hint_y=None, height=dp(50), halign='left', valign='middle')
        heading.bind(size=heading.setter('text_size')) # Bind text_size for alignment
        list_area_layout.add_widget(heading)

        self.list_display = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.list_display.bind(minimum_height=self.list_display.setter('height'))
        # ScrollView takes up the remaining vertical space in list_area_layout
        scroll_view = ScrollView(size_hint_y=1)
        scroll_view.add_widget(self.list_display)
        list_area_layout.add_widget(scroll_view)

        # Add list_area_layout first
        self.add_widget(list_area_layout)

        # Button area
        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            orientation='horizontal',
            padding=dp(5),
            spacing=dp(10))
        add_button = Button(text="New List")
        add_button.bind(on_press=self.add_list)
        ai_button = Button(text='Make List with AI')
        ai_button.bind(on_press=self._prompt_ai)
        button_layout.add_widget(add_button)
        button_layout.add_widget(ai_button)
        self.button_layout = button_layout

        # Add button_layout second
        self.add_widget(button_layout)

        # Overlay
        self.overlay_layout = FloatLayout()
        self.loading_image = Image(
            source='gui/thinking_anim.gif',
            size_hint=(None, None),
            size=(dp(200), dp(200)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.01,
            anim_loop = 0,
            opacity=0 # Starts out hidden
        )
        self.overlay_layout.add_widget(self.loading_image)

        # Populate task list
        self.refresh_list()


    def refresh_list(self):
        self.list_display.clear_widgets()
        for list_obj in self.master_list.lists:
            list_item = ListItem(
                                 list_obj, # Pass the actual list object
                                 on_edit=self.edit_list,
                                 on_delete=self.delete_list,
                                 on_open=self.open_list,
                                 size_hint_y=None,
                                 height=dp(75)
                                 )
            self.list_display.add_widget(list_item)

    def _show_loading(self, show=True):
        """Helper to show/hide loading overlay."""
        if show:
            if self.overlay_layout not in self.children:
                self.add_widget(self.overlay_layout)
            self.loading_image.opacity = 1
            self.button_layout.disabled = True
            for item in self.list_display.children:
                 item.disabled = True
        else:
            self.loading_image.opacity = 0
            if self.overlay_layout in self.children:
                self.remove_widget(self.overlay_layout)
            self.button_layout.disabled = False
            # Reenable list items
            for item in self.list_display.children:
                 item.disabled = False

    def save_ai_list(self, ai_data):
        """Starts the AI list creation process in a separate thread."""
        self._show_loading(True) # Shows animation

        thread = threading.Thread(
            target=self._perform_ai_list_creation,
            args=(ai_data,)
        )
        thread.daemon = True
        thread.start()

    def _perform_ai_list_creation(self, ai_data):
        """Runs the blocking AI call and processing in the background thread."""
        try:
            ai_title = ai_data['Title']
            ai_text = AICaller().make_AI_tasklist(ai_data['Prompt'])
            new_file_path = JsonGenerator.string_to_json(self, title=ai_title, content=ai_text)
            new_json_manager = JsonManager(new_file_path)
            new_list = TaskList(ai_title, new_json_manager)
            Clock.schedule_once(lambda dt: self._on_ai_list_created(new_list, None))
        except Exception as e:
            print(f"Thread: Error during AI list creation: {e}")
            Clock.schedule_once(lambda dt: self._on_ai_list_created(None, e))

    def _on_ai_list_created(self, new_list, error):
        """Runs on the main Kivy thread after the background thread finishes."""
        self._show_loading(False) # Hide animation

        if error:
            print(f"MainThread: AI Error - {error}")
        elif new_list:
            self.master_list.add_list(new_list)
            self.refresh_list()
        else:
             print("MainThread: Unknown state in AI callback.")

    def _prompt_ai(self, instance):
        form = AIFormModal(on_save=self.save_ai_list)
        form.open()

    def add_list(self, instance):
        form = ListFormModal(on_save=self.save_new_list)
        form.open()

    def edit_list(self, list_obj, new_title):
        # Check if the title actually changed
        if list_obj.title == new_title or not new_title.strip():
             print("Title unchanged or empty, edit cancelled.")
             self.refresh_list() # Refreshes to collapse the item
             return

        # validation for filename safety
        safe_title = "".join(c for c in new_title if c.isalnum() or c in (' ', '_')).rstrip()
        if not safe_title:
             print("Invalid new title provided.")
             self.refresh_list()
             return

        old_file_path = list_obj.json_manager.file_path
        new_file_path = safe_title + ".json"

        if old_file_path == new_file_path:
            print("Filename is the same, only updating title.")
            list_obj.title = new_title # Update title in the object
            list_obj.update_json() # Save potential task changes within the existing file
            self.master_list.update_json() # Save the updated title in masterlist.json
            self.refresh_list()
            return

        try:
            import os
            if os.path.exists(new_file_path):
                 print(f"Error: File '{new_file_path}' already exists. Cannot rename.")
                 self.refresh_list()
                 return
            os.rename(old_file_path, new_file_path)
            print(f"Renamed file '{old_file_path}' to '{new_file_path}'")

            # Now update the list object and save the master list
            list_obj.title = new_title
            list_obj.json_manager.file_path = new_file_path
            self.master_list.update_json() # Save changes to masterlist.json
            self.refresh_list()

        except OSError as e:
            print(f"Error renaming file: {e}")
            self.refresh_list() # Refresh even on error to collapse item


    def delete_list(self, list_obj):
        import os
        try:
            file_to_delete = list_obj.json_manager.file_path
            self.master_list.delete_list(list_obj.title) # Remove from master list first
            if os.path.exists(file_to_delete):
                 os.remove(file_to_delete) # Delete associated JSON file
                 print(f"Deleted file: {file_to_delete}")
            else:
                 print(f"Warning: File not found, could not delete: {file_to_delete}")
            self.refresh_list()
        except Exception as e:
             print(f"Error deleting list or file: {e}")
             self.refresh_list()


    def save_new_list(self, new_title):
        # title validation
        safe_title = "".join(c for c in new_title if c.isalnum() or c in (' ', '_')).rstrip()
        if not safe_title:
             print("Invalid list title.")
             return

        # Check if list already exists
        if self.master_list.get_list(safe_title):
            print(f"List '{safe_title}' already exists.")
            return

        try:
            new_file_path = JsonGenerator().new_json(title=safe_title)
            new_json_manager = JsonManager(new_file_path)
            new_list = TaskList(safe_title, new_json_manager)
            self.master_list.add_list(new_list)
            self.refresh_list()
        except Exception as e:
            print(f"Error creating new list: {e}")

    @staticmethod
    def open_list(lst):
        app = App.get_running_app()
        if hasattr(app, 'set_return_and_stop'):
             app.set_return_and_stop(lst)
        elif hasattr(app, 'set_return'):
             app.set_return(lst)
             app.stop()
        else:
            print("Error: Could not find method to return list and stop app.")


