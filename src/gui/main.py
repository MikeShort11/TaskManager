import pages.add_screen as add_screen
import pages.main_screen as main_screen
import pages.edit_screen as edit_screen


from utils.task_list import TaskList

task_manager = TaskList('utils/tasks.json')

def add(task_manager_list):
    to_add = add_screen.MainApp().run()
    

def delete(task_manager_list, title):
    #TODO: fix delete so it accutally deletes
    task_manager_list.delete_task(title)

def edit(task_manager_list):
    #TODO: allow for editin and deletin
    edit_screen.MainApp().run()

def main():
    while True:
        first_in = main_screen.MainApp().run()
        print(first_in)
        command_dict = {"add": lambda: add(task_manager),
                        "delete": lambda: delete(task_manager, first_in),
                        "edit": lambda: edit(task_manager),
                        "quit": lambda: exit(),
                        }
        try:
            command_dict[first_in[0]]()
        except:
            print("error with first_in")



if __name__ == "__main__":
    main()
