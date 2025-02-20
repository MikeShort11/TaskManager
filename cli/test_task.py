from task import Task

test_task = Task("task1")

def test_create_task():
    """Test if task construction works as intended at the class level."""
    assert test_task.title == "task1"
    assert test_task.date == "no date"
    assert test_task.time == "no time"
    assert test_task.description == "enter description here"
    assert test_task.category == "no category"

def test_str():
    assert test_task.__str__() == " task1, no date, no time, enter description here, no category"
