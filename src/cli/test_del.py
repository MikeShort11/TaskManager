from task_list import TaskList

test_list = TaskList()

def test_delete_empty():
    assert test_list.delete_task("example 1") == "Key not found!"


def test_delete():

    test_list.add_task("example 1")
    test_list.delete_task("example 1")
    assert print(test_list) == "No tasks found in this list."

    test_list.add_task("example 2")
    test_list.add_task("example 3")
    test_list.add_task("example 4")
    test_list.add_task("example 5")
    test_list.delete_task("example 4")
    assert print(test_list) == "example 2, example 3, example 5"


