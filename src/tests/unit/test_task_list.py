"""
Tests the task_list class and all its member functions.


Tests the edit method of the task class.

task.edit(attribute, value)

attribute is the attribute of the instance you are editing
value is what the attribute is being changed to
"""

from datetime import date
from task_list import TaskList

test_list = TaskList()

def test_add_task():
    """Tests if the add function actually adds the task properly."""
    assert test_list.size == 0
    assert test_list.add_task("task1") == "task1 task added successfully."
    assert test_list.size == 1

def test_add_duplicate_task():
    """Function should return early if task name is already in use."""
    assert test_list.add_task("task1") == "'task1' is taken, try another name."
    assert test_list.size == 1

def test_delete():
    """Tests for expected behavior of successful task deletion."""
    test_list.add_task("task1")
    assert test_list.size == 1
    assert test_list.delete_task("task1") == "task1 deleted."
    assert test_list.size == 0

    test_list.add_task("task2")
    test_list.add_task("task3")
    test_list.add_task("task4")
    test_list.add_task("task5")
    test_list.delete_task("task4")
    assert test_list.size == 3
    assert test_list.__str__() == "task2, task3, task5"

def test_delete_missing():
    """Tests for proper behavior from delete if the task isn't found."""
    assert test_list.delete_task("task1") == "Key not found!"
    assert test_list.size == 3



"""
test_task = Task("test", date(1025, 2, 15), "a task to test the edit metod", "school")

def test_edit_description():
    assert test_task.description == "a task to test the edit metod"
    test_task.edit_task(descrption, "new description")
    assert test_task.description == "new description"

def test_edit_datetime():
    assert test_task.datetime == date(1025, 2, 15)
    test_task.edit_task(datetime, date(2025, 2, 15))
    assert test_task.datetime == date(2025, 2, 15)

def test_edit_catergory():
    assert test_task.catergory == "school"
    test_task.edit_task(catergory, "work")
    assert test_task.description == "work"


"""


