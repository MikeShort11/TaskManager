from task_list import TaskList

task_manager = TaskList('C:/Users/gturt/PycharmProjects/TaskManager/src/gui/utils/tasks.json')
print(task_manager)
task_manager.add_task("Test Task2")
task_manager.add_task("Test Task3")
print(task_manager)