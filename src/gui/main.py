import pages.add_screen as add_screen
import pages.main_screen as main_screen
import pages.edit_screen as edit_screen


from utils.task_list import TaskList

task_manager = TaskList('utils/tasks.json')

def add(task_manager_list):
    add_dict = add_screen.MainApp().run()
    task_manager_list.add_task(add_dict["title"], add_dict["date"],
                               add_dict["time"], add_dict["category"],
                               add_dict["description"])


def delete(task_manager_list, title):
    task_manager_list.delete_task(title)

def edit(task_manager_list, title):
    add_dict = edit_screen.MainApp().run()
    for key in add_dict:
        if add_dict[key] == "":
            add_dict[key] = task_manager_list.list[title].to_dict()[key]
    task_manager_list.delete_task(title)
    task_manager_list.add_task(add_dict["title"], add_dict["date"],
                               add_dict["time"], add_dict["category"],
                               add_dict["description"])

def main():
    keep_running = True
    while keep_running == True:
        first_in = main_screen.MainApp().run()
        print(first_in[1])
        command_dict = {"add": lambda: add(task_manager),
                        "delete": lambda: delete(task_manager, first_in[1]),
                        "edit": lambda: edit(task_manager, first_in[1]),
                        }

        # keep_running = False

        try:
            if first_in == "none":
                keep_running = False
            else:
                command_dict[first_in[0]]()
                print(first_in[0])

        except:
            print("error with first_in")


    main_screen.MainApp().stop()



if __name__ == "__main__":
    main()
