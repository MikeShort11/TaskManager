from task_list import TaskList

test_list = TaskList()

def test_delete_empty():
    assert test_list.delete_task("example 1") == KeyError

def test_delete():

    test_list.add_task("example 1")
    test_list.delete_task("example 1")
    assert str(test_list) == "Empty"

    test_list.add_task("example 2")
    test_list.add_task("example 3")
    test_list.add_task("example 4")
    test_list.add_task("example 5")
    test_list.delete_task("example 4")
    assert str(test_list) == "example 2, example 3, example 5"


