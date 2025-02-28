from kivy.app import App, Builder
#layout imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#widget layouts
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView




class TopLabel(BoxLayout):
    """the Label at the top of the page"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y=0.1
        self.orientation = "vertical"
        self.top_label = Label(text="Top Label")
        self.add_widget(self.top_label)

class ListDisplay(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #the sroller layout
        list_of_tasks = GridLayout(cols=1, size_hint_y=None)  
        list_of_tasks.bind(minimum_height=list_of_tasks.setter('height'))  # Ensure it resizes correctly


        #some temporary text for testing the layouts
        #temp_list = ["hello", "world"]
        #temp_list = ["hello", "world", "text", "to", "fill", "space"]
        temp_list = ["hello", "world", "text", "to", "fill", "space", "even", "more", "txt", "hello", "world", "text", "to", "fill", "space", "even", "more", "txt"]

        #loop through the data to get the labels for the tasks
        for i in temp_list:
            task = BoxLayout(orientation='horizontal', size_hint_y=None, size=(100, 75))
            lbl = Label(text=i) #the text for the task
            btn = Button(text="expand", size_hint_x=0.1) #the button to expand the task
            #add the items to the larger layout
            task.add_widget(btn)
            task.add_widget(lbl)
            list_of_tasks.add_widget(task)

        self.add_widget(list_of_tasks)
        #TODO: add the drop down info

class MainApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")

        top_label_widget = TopLabel()
        list_display_widget = ListDisplay()

        root.add_widget(top_label_widget)
        root.add_widget(list_display_widget)

        return root

if __name__ == '__main__':
    MainApp().run()

