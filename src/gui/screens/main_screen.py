from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App

from .task_form_screen import TaskFormModal
from ..utils.task import Task
import functools

def compare_by_priority(task_one: Task, task_two: Task):
    """Sets the task order based on priority."""
    try:
        p1 = int(task_one.priority)
        p2 = int(task_two.priority)
        if p1 < p2: return -1
        elif p1 > p2: return 1
        else: return 0
    except (ValueError, TypeError):
        return 0


class TaskItem(BoxLayout):
    def __init__(self, task, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.task = task
        self.on_delete = on_delete
        self.on_edit = on_edit
        self._collapsed_height = kwargs.get('height', dp(75))
        self._expanded_height_min = dp(200)
        self._bottom_container = None # the expanded content widget

        # Top half setup
        top_half = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        top_half.add_widget(Label(text=task.title))
        self.expand_button = Button(on_press=self.expand_and_collapse, text='Expand', size_hint_x=0.3)
        top_half.add_widget(self.expand_button)
        self.add_widget(top_half)

    def expand_and_collapse(self, instance):
        """Logic for the collapse and expand buttons for the tasks."""
        task_item = self
        task = task_item.task

        # Prevents issues from rapid double-clicks
        instance.disabled = True
        # Reenable after short delay
        Clock.schedule_once(lambda dt: setattr(instance, 'disabled', False), 0.2)

        if self._bottom_container is not None: # If expanded
            # Collapse logic
            task_item.remove_widget(self._bottom_container)
            self._bottom_container = None # Clear container
            task_item.height = self._collapsed_height
            task_item.size_hint_y = None
            instance.text = "Expand"
        else: # If collapsed
            # Expand logic
            # 1. Immediately set minimum expanded height and update button text
            task_item.height = self._expanded_height_min
            task_item.size_hint_y = None
            instance.text = "Collapse"

            # 2. Schedule the creation and addition of the actual content
            def add_content(dt):
                # Double check it wasn't collapsed again before this triggers
                if self._bottom_container is not None or instance.text != "Collapse":
                    return

                # Create bottom_container and its contents
                self._bottom_container = BoxLayout(
                    orientation='vertical', padding=(dp(10), dp(10)),
                    spacing=dp(10), size_hint_y=None
                )
                self._bottom_container.bind(minimum_height=self._bottom_container.setter('height'))

                details_layout = GridLayout(
                    cols=2, size_hint_y=None, row_default_height=dp(25),
                    row_force_default=False, spacing=(dp(10), dp(5))
                )
                details_layout.bind(minimum_height=details_layout.setter('height'))

                def add_detail_row(field_name, field_value, is_long_text=False):
                    name_label = Label(text=f"[b]{field_name}:[/b]",
                                       markup=True, size_hint=(None, None),
                                       width=dp(100),
                                       height=dp(25) if not is_long_text else dp(20),
                                       halign='right', valign='top',
                                       text_size=(dp(100),
                                                  None))
                    details_layout.add_widget(name_label)
                    value_label = Label(text=str(field_value),
                                        size_hint_y=None,
                                        height=dp(25) if not is_long_text else dp(20),
                                        halign='left',
                                        valign='top')
                    value_label.bind(width=lambda *x: value_label.setter('text_size')(value_label, (value_label.width, None)),
                                     texture_size=lambda *x: value_label.setter('height')(value_label, value_label.texture_size[1]))
                    details_layout.add_widget(value_label)
                    if is_long_text:
                        def sync_heights(*args): name_label.height = max(dp(20), value_label.height)
                        value_label.bind(height=sync_heights)

                add_detail_row("Description", task.description, is_long_text=True)
                add_detail_row("Date", task.date)
                add_detail_row("Time", task.time)
                add_detail_row("Priority", task.priority)
                self._bottom_container.add_widget(details_layout)

                button_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
                edit_button = Button(text="Edit", background_color=(0.2, 0.6, 0.2, 1))
                edit_button.bind(on_press=lambda inst: self.on_edit(task))
                button_row.add_widget(edit_button)
                delete_button = Button(text="Delete", background_color=(0.8, 0.2, 0.2, 1))
                delete_button.bind(on_press=lambda inst: self.on_delete(task))
                button_row.add_widget(delete_button)
                self._bottom_container.add_widget(button_row)

                # Adds the created container to the TaskItem
                task_item.add_widget(self._bottom_container, index=0)

                # 3. Schedule final height adjustment *after* content is added
                def finish_height_adjustment(dt2):
                    """Check if still expanded and content exists, then change height."""
                    if self._bottom_container and self._bottom_container in task_item.children:
                         try:
                             top_h = task_item.children[1].height
                             bottom_h = self._bottom_container.height
                             required_height = top_h + bottom_h + dp(10)
                             task_item.height = max(self._expanded_height_min, required_height)
                             task_item.size_hint_y = None # Reaffirm
                         except IndexError:
                              print("Error accessing children during height adjustment - possibly collapsed quickly.")

                Clock.schedule_once(finish_height_adjustment, 0.01) # Tiny delay

            Clock.schedule_once(add_content, 0)


class MainScreen(BoxLayout):
    def __init__(self, task_list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.task_list = task_list
        self.is_sorted = False
        self.revert_list = self.task_list.tasks.copy() if hasattr(self.task_list, 'tasks') and self.task_list.tasks else []

        # Heading Area for Back button
        heading_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )

        # Title label
        title_text = task_list.title if task_list and hasattr(task_list, 'title') else "Task List"
        title_label = Label(
            text=title_text,
            font_size="40sp",
            size_hint_x=0.9,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size')) # Needed for alignment
        heading_layout.add_widget(title_label)

        # Back button
        back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(dp(90), dp(45)),  # fixed size
        )
        back_button.bind(on_press=self.go_back)
        heading_layout.add_widget(back_button)

        self.add_widget(heading_layout)

        # ScrollView
        self.task_display = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5), padding=(dp(5),0))
        self.task_display.bind(minimum_height=self.task_display.setter('height'))
        scroll_view = ScrollView(size_hint_y=1)
        scroll_view.add_widget(self.task_display)
        self.add_widget(scroll_view)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5), spacing=dp(10))
        add_button = Button(text="Add Task")
        add_button.bind(on_press=self.add_task)
        button_layout.add_widget(add_button)
        sort_button = Button(text="Priority Sort")
        sort_button.bind(on_press=self.sort_tasks_button)
        button_layout.add_widget(sort_button)
        self.add_widget(button_layout)

        # Initial Refresh
        Clock.schedule_once(self.refresh_task_list)

    def go_back(self, instance):
        """Stops the current TaskListApp instance."""
        print("Back button pressed - stopping TaskListApp")
        # Stops the current running app which represents the tasks view
        app = App.get_running_app()
        app.stop()

    def refresh_task_list(self, *args):
        self.task_display.clear_widgets()
        tasks_to_display = []
        # Safely accesses tasks
        current_tasks = self.task_list.tasks if hasattr(self.task_list, 'tasks') and self.task_list.tasks else []

        if self.is_sorted:
            try:
                key = functools.cmp_to_key(compare_by_priority)
                tasks_to_display = sorted(current_tasks, key=key)
            except Exception as e:
                print(f"Error during sorting: {e}")
                tasks_to_display = current_tasks # Fallback
        else:
            tasks_to_display = current_tasks

        # Create and add TaskItems
        for task in tasks_to_display:
            if isinstance(task, Task):
                 task_item = TaskItem(
                                      task,
                                      on_edit=self.edit_task,
                                      on_delete=self.delete_task,
                                      size_hint_y=None,
                                      height=dp(75)
                                      )
                 self.task_display.add_widget(task_item)
            else:
                 print(f"Warning: Item is not a Task object: {task}")

        # Update revert_list
        if not self.is_sorted:
             self.revert_list = current_tasks.copy()


    def add_task(self, instance):
        form = TaskFormModal(on_save=self.save_new_task)
        form.open()

    def edit_task(self, task):
        form = TaskFormModal(task, on_save=self.save_edited_task)
        form.open()

    def delete_task(self, task_to_delete):
        if not hasattr(self.task_list, 'tasks'): return
        original_title = task_to_delete.title
        self.task_list.delete_task(original_title)
        self.revert_list = [task for task in self.revert_list if task.title != original_title]
        self.refresh_task_list()

    def save_new_task(self, task_data):
        try:
            if not task_data.get('title'):
                print("Error: Task title cannot be empty.")
                return
            new_task = Task(**task_data)
            self.task_list.add_task(new_task)
            if not self.is_sorted:
                 self.revert_list.append(new_task)
            self.refresh_task_list()
        except Exception as e: print(f"Error saving new task: {e}")

    def save_edited_task(self, task_data):
        try:
            title = task_data.get('title')
            if not title: print("Error: Task title cannot be empty."); return

            # Find original task
            original_task = next((t for t in self.task_list.tasks if t.title == title), None)
            if not original_task: print(f"Error: Cannot find task with title '{title}'"); return

            for key, value in task_data.items(): setattr(original_task, key, value)
            self.task_list.update_json()

            # Update revert list too
            for i, task in enumerate(self.revert_list):
                if task.title == title: # Assumes title hasn't changed
                    for key, value in task_data.items(): setattr(self.revert_list[i], key, value)
                    break
            self.refresh_task_list()
        except Exception as e: print(f"Error saving edited task: {e}")

    def sort_tasks_button(self, instance):
        current_tasks = self.task_list.tasks if hasattr(self.task_list, 'tasks') and self.task_list.tasks else []
        if not current_tasks: print("No tasks to sort."); return

        if not self.is_sorted:
            self.is_sorted = True
            instance.text = "'Original Order' Sort"
        else:
            self.is_sorted = False
            instance.text = "Priority Sort"
        self.refresh_task_list()
