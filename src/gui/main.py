import pages.add_screen as add_screen
import pages.main_screen as main_screen
import pages.edit_screen as edit_screen


from utils.task_list import TaskList

task_manager = TaskList('utils/tasks.json')

def main():
    first_in = main_screen.MainApp().run()
    print(first_in)



if __name__ == "__main__":
    main()
