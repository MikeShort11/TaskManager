from task import Task
from task_list import TaskList
from task_list import JsonManager
import functools

data = JsonManager('test.json')
task_list = TaskList(data)

def category_comparator(task_one: Task, task_two: Task):
    if int(task_one.category) < int(task_two.category):
        return -1
    elif int(task_one.category) > int(task_two.category):
        return 1
    else:
        return 0



test_task1 = Task("Taco", category="10")
test_task2 = Task("Cheeseburger", category="7")
test_task3 = Task("Pizza", category="3")
test_task4 = Task("Chicken", category="2")

task_list.add_task(test_task1)
task_list.add_task(test_task2)
task_list.add_task(test_task3)
task_list.add_task(test_task4)

print("NOT SORTED")
for task in task_list.tasks:
    print(task.title)

key=functools.cmp_to_key(category_comparator)

# task_list.tasks = sorted(task_list.tasks, key=key)
task_list.sort_tasks(key)

print("SORTED")
for task in task_list.tasks:
    print(task.title)

# task_list.delete_task("Taco")
# task_list.delete_task("Cheeseburger")
# task_list.delete_task("Pizza")
# task_list.delete_task("Chicken")


