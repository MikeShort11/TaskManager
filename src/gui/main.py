import pages.add_screen as add_screen
import pages.main_screen as main_screen
import pages.edit_screen as edit_screen


from utils.task_list import TaskList

task_manager = TaskList('utils/tasks.json')

def add(task_manager_list):
    add_dict = add_screen.MainApp().run()
    task_manager_list.add_task(add_dict["Title"], add_dict["Date"],
                               add_dict["Time"], add_dict["Category"],
                               add_dict["Description"])

def delete(task_manager_list, title):
    #TODO: fix delete so it actually deletes
    task_manager_list.delete_task(title)

def edit(task_manager_list):
    #TODO: allow for editin and deletin
    edit_screen.MainApp().run()

def main():
    keep_running = True
    while keep_running == True:
        first_in = main_screen.MainApp().run()
        print(first_in)
        command_dict = {"add": lambda: add(task_manager),
                        "delete": lambda: delete(task_manager, first_in),
                        "edit": lambda: edit(task_manager),
                        }

        # keep_running = False

        try:
            if first_in == "none":
                keep_running = False
            else:
                command_dict[first_in[0]]()
                main_screen.MainApp().run()
        except:
            print("error with first_in")


    main_screen.MainApp().stop()



if __name__ == "__main__":
    main()
