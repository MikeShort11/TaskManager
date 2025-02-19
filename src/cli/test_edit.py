"""
Tests the edit method of the task class.

task.edit(attribute, value)

attribute is the attribute of the instance you are editing
value is what the attribute is being changed to
"""

from datetime import date
from main.py import Task

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

