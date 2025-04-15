# test_taskmanager.py
import pytest
import os
import json
from pathlib import Path

from src.gui.utils.task import Task
from src.gui.utils.task_list import JsonManager, TaskList
from src.gui.utils.list_list import ListJsonManager, ListList

# Dummy data

@pytest.fixture
def sample_task_data():
    """Provides sample data for creating a Task."""
    return {
        "title": "Test Task 1",
        "date": "2025-04-15",
        "time": "10:00",
        "description": "This is a test description.",
        "priority": "3"
    }

@pytest.fixture
def sample_task(sample_task_data):
    """Provides a Task instance."""
    return Task(**sample_task_data)

@pytest.fixture
def temp_json_file(tmp_path):
    """Creates a temporary JSON file path."""
    return tmp_path / "test_tasks.json"

@pytest.fixture
def temp_master_json_file(tmp_path):
    """Creates a temporary master list JSON file path."""
    return tmp_path / "test_masterlist.json"

@pytest.fixture
def populated_json_manager(temp_json_file, sample_task):
    """Provides a JsonManager with a pre-populated temporary file."""
    manager = JsonManager(str(temp_json_file))
    manager.tasks = [sample_task]
    manager.save_tasks()
    # Return a new manager instance pointing to the same populated file
    return JsonManager(str(temp_json_file))

@pytest.fixture
def sample_task_list(populated_json_manager):
    """Provides a TaskList instance based on the populated JsonManager."""
    return TaskList("My Test List", populated_json_manager)

@pytest.fixture
def populated_list_json_manager(temp_master_json_file, sample_task_list):
    """Provides a ListJsonManager with a pre-populated master file."""
    list_manager = ListJsonManager(str(temp_master_json_file))
    # Manually create the task list dictionary structure expected by ListList.to_dict
    # and save it using the ListJsonManager's internal structure expectation
    list_manager.lists = [sample_task_list] # Store the TaskList object directly
    list_manager.save_lists()
    # Return a new manager instance pointing to the same populated file
    return ListJsonManager(str(temp_master_json_file))

@pytest.fixture
def sample_list_list(populated_list_json_manager):
    """Provides a ListList instance based on the populated ListJsonManager."""
    return ListList(populated_list_json_manager)


# Task Tests

def test_task_init(sample_task_data):
    """Test Task initialization."""
    task = Task(**sample_task_data)
    assert task.title == sample_task_data["title"]
    assert task.date == sample_task_data["date"]
    assert task.time == sample_task_data["time"]
    assert task.description == sample_task_data["description"]
    assert task.priority == sample_task_data["priority"]

def test_task_init_defaults():
    """Test Task initialization with default values."""
    task = Task(title="Only Title")
    assert task.title == "Only Title"
    assert task.date == ""
    assert task.time == ""
    assert task.description == ""
    assert task.priority == ""

def test_task_to_dict(sample_task, sample_task_data):
    """Test Task to_dict method."""
    assert sample_task.to_dict() == sample_task_data

def test_task_from_dict(sample_task_data):
    """Test Task from_dict class method."""
    task = Task.from_dict(sample_task_data)
    assert task.title == sample_task_data["title"]
    assert task.date == sample_task_data["date"]
    assert task.time == sample_task_data["time"]
    assert task.description == sample_task_data["description"]
    assert task.priority == sample_task_data["priority"]

# Json tests

def test_json_manager_init_new_file(temp_json_file):
    """Test JsonManager initialization with a non-existent file."""
    manager = JsonManager(str(temp_json_file))
    assert manager.file_path == str(temp_json_file)
    assert manager.tasks == []

def test_json_manager_load_tasks(populated_json_manager, sample_task_data):
    """Test JsonManager loading tasks from an existing file."""
    assert len(populated_json_manager.tasks) == 1
    loaded_task = populated_json_manager.tasks[0]
    assert isinstance(loaded_task, Task)
    assert loaded_task.title == sample_task_data["title"]

def test_json_manager_save_tasks(temp_json_file, sample_task_data):
    """Test JsonManager saving tasks to a file."""
    manager = JsonManager(str(temp_json_file))
    task1 = Task.from_dict(sample_task_data)
    task2_data = sample_task_data.copy()
    task2_data["title"] = "Test Task 2"
    task2 = Task.from_dict(task2_data)

    manager.tasks = [task1, task2]
    manager.save_tasks()

    assert os.path.exists(temp_json_file)
    with open(temp_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["title"] == "Test Task 1"
    assert data[1]["title"] == "Test Task 2"

# TaskList tests

def test_task_list_init(sample_task_list, populated_json_manager):
    """Test TaskList initialization."""
    assert sample_task_list.title == "My Test List"
    assert sample_task_list.json_manager == populated_json_manager
    assert len(sample_task_list.tasks) == 1
    assert sample_task_list.tasks[0].title == "Test Task 1"

def test_task_list_add_task(sample_task_list, temp_json_file):
    """Test adding a task to TaskList."""
    initial_count = len(sample_task_list.tasks)
    new_task = Task(title="New Task")
    sample_task_list.add_task(new_task)

    assert len(sample_task_list.tasks) == initial_count + 1
    assert sample_task_list.tasks[-1].title == "New Task"

    # Verify JSON file was updated
    with open(temp_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == initial_count + 1
    assert data[-1]["title"] == "New Task"

def test_task_list_delete_task(sample_task_list, temp_json_file):
    """Test deleting a task from TaskList."""
    task_to_delete = sample_task_list.tasks[0].title
    initial_count = len(sample_task_list.tasks)

    sample_task_list.delete_task(task_to_delete)

    assert len(sample_task_list.tasks) == initial_count - 1
    assert all(task.title != task_to_delete for task in sample_task_list.tasks)

    # Verify JSON file was updated
    with open(temp_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == initial_count - 1

def test_task_list_get_task(sample_task_list):
    """Test getting a task from TaskList."""
    task_title = sample_task_list.tasks[0].title
    task = sample_task_list.get_task(task_title)
    assert task is not None
    assert task.title == task_title

    non_existent_task = sample_task_list.get_task("NonExistentTask")
    assert non_existent_task is None

def test_task_list_sort_tasks(sample_task_list):
    """Test sorting tasks in TaskList."""
    task2 = Task(title="Task B", priority="1")
    task3 = Task(title="Task C", priority="5")
    sample_task_list.add_task(task2)  # Original task has priority 3
    sample_task_list.add_task(task3)

    # Sort by priority (lower number = higher priority)
    sample_task_list.sort_tasks(lambda t: int(t.priority) if t.priority.isdigit() else 999)

    assert sample_task_list.tasks[0].title == "Task B" # Priority 1
    assert sample_task_list.tasks[1].title == "Test Task 1"  # Priority 3
    assert sample_task_list.tasks[2].title == "Task C"  # Priority 5

def test_task_list_to_dict(sample_task_list):
    """Test TaskList to_dict method."""
    expected_dict = {
        "title": "My Test List",
        "JSON": sample_task_list.json_manager.file_path
    }
    assert sample_task_list.to_dict() == expected_dict

def test_task_list_from_dict(populated_json_manager):
    """Test TaskList from_dict class method."""
    list_data = {
        "title": "Loaded List",
        "JSON": populated_json_manager.file_path
    }
    loaded_list = TaskList.from_dict(list_data)
    assert loaded_list.title == "Loaded List"
    assert loaded_list.json_manager.file_path == populated_json_manager.file_path
    assert len(loaded_list.tasks) == 1  # Should load tasks via JsonManager
    assert loaded_list.tasks[0].title == "Test Task 1"


# ListJsonManager Tests

def test_list_json_manager_init_new_file(temp_master_json_file):
    """Test ListJsonManager initialization with a non-existent file."""
    manager = ListJsonManager(str(temp_master_json_file))
    assert manager.file_path == str(temp_master_json_file)
    assert manager.lists == []

def test_list_json_manager_load_lists(populated_list_json_manager, sample_task_list):
    """Test ListJsonManager loading lists from an existing file."""
    assert len(populated_list_json_manager.lists) == 1
    loaded_list = populated_list_json_manager.lists[0]
    assert isinstance(loaded_list, TaskList)
    assert loaded_list.title == sample_task_list.title
    assert loaded_list.json_manager.file_path == sample_task_list.json_manager.file_path
    assert len(loaded_list.tasks) == 1 # Check tasks were loaded within the TaskList

def test_list_json_manager_save_lists(temp_master_json_file, temp_json_file):
    """Test ListJsonManager saving lists to a file."""
    # Create two distinct task lists
    manager1 = JsonManager(str(temp_json_file))
    list1 = TaskList("List One", manager1)
    list1.add_task(Task("Task A"))

    json_path2 = Path(str(temp_json_file)).parent / "test_tasks2.json"
    manager2 = JsonManager(str(json_path2))
    list2 = TaskList("List Two", manager2)
    list2.add_task(Task("Task B"))

    # Create ListJsonManager and save
    list_manager = ListJsonManager(str(temp_master_json_file))
    list_manager.lists = [list1, list2]
    list_manager.save_lists()

    # Verify master file content
    assert os.path.exists(temp_master_json_file)
    with open(temp_master_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["title"] == "List One"
    assert data[0]["JSON"] == str(temp_json_file)
    assert data[1]["title"] == "List Two"
    assert data[1]["JSON"] == str(json_path2)


# ListList Tests

def test_list_list_init(sample_list_list, populated_list_json_manager):
    """Test ListList initialization."""
    assert sample_list_list.json_manager == populated_list_json_manager
    assert len(sample_list_list.lists) == 1
    assert sample_list_list.lists[0].title == "My Test List"

def test_list_list_add_list(sample_list_list, temp_master_json_file, tmp_path):
    """Test adding a list to ListList."""
    initial_count = len(sample_list_list.lists)

    # Create a new task list to add
    new_list_json_path = tmp_path / "new_list_tasks.json"
    new_manager = JsonManager(str(new_list_json_path))
    new_list = TaskList("Newly Added List", new_manager)
    new_list.add_task(Task("Task X")) # Add a task to make it non-empty

    sample_list_list.add_list(new_list)

    assert len(sample_list_list.lists) == initial_count + 1
    assert sample_list_list.lists[-1].title == "Newly Added List"
    assert len(sample_list_list.lists[-1].tasks) == 1

    # Verify master JSON file was updated
    with open(temp_master_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == initial_count + 1
    assert data[-1]["title"] == "Newly Added List"
    assert data[-1]["JSON"] == str(new_list_json_path)

def test_list_list_delete_list(sample_list_list, temp_master_json_file):
    """Test deleting a list from ListList."""
    list_to_delete = sample_list_list.lists[0].title
    initial_count = len(sample_list_list.lists)

    sample_list_list.delete_list(list_to_delete)

    assert len(sample_list_list.lists) == initial_count - 1
    assert all(lst.title != list_to_delete for lst in sample_list_list.lists)

    # Verify master JSON file was updated
    with open(temp_master_json_file, 'r') as f:
        data = json.load(f)
    assert len(data) == initial_count - 1

def test_list_list_get_list(sample_list_list):
    """Test getting a list from ListList."""
    list_title = sample_list_list.lists[0].title
    lst = sample_list_list.get_list(list_title)
    assert lst is not None
    assert lst.title == list_title

    non_existent_list = sample_list_list.get_list("NonExistentList")
    assert non_existent_list is None
