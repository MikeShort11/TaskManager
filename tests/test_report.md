# Test Artifacts - Milestone 5

## test_taskmanager.py
Step 1: Creates fixtures to represent dummy objects for testing purposes.

- sample_task_data()
- sample_task(sample_task_data)
- temp_json_file(tmp_path)
- temp_master_json_file(tmp_path)
- populated_json_manager(temp_json_file, sample_task)
- sample_task_list(populated_json_manager)
- populated_list_json_manager(temp_master_json_file, sample_task_list)
- sample_test_list(populated_list_json_manager)

Step 2: Unit tests

### test_task_init()
- Purpose: Verify Task init assigns provided values.
- Input: Task data dictionary.
- Output: Task object matching input.
- Expected: Task created with correct attributes.
- Actual: Correct Task created. 
**PASS**

### test_task_init_defaults()
- Purpose: Verify Task init uses defaults for missing attributes.
- Input: Dictionary with 'title' only.
- Output: Task object with title and default empty strings.
- Expected: Task created with defaults applied.
- Actual: Correct Task with defaults created. 
**PASS**

### test_task_to_dict()
- Purpose: Verify `to_dict` returns correct dictionary.
- Input: Task object.
- Output: Dictionary matching Task attributes.
- Expected: Dictionary accurately represents Task.
- Actual: Correct dictionary returned. 
**PASS**

### test_task_from_dict()
- Purpose: Verify `from_dict` creates Task from dictionary.
- Input: Task data dictionary.
- Output: Task object matching dictionary.
- Expected: Task object created accurately.
- Actual: Correct Task object created. 
**PASS**

## JsonManager Tests (src.gui.utils.task_list.JsonManager)

### test_json_manager_init_new_file()
- Purpose: Verify JsonManager init with non-existent file.
- Input: Path to non-existent JSON.
- Output: JsonManager with correct path, empty task list.
- Expected: JsonManager initialized, empty tasks.
- Actual: Initialized correctly. 
**PASS**

### test_json_manager_load_tasks()
- Purpose: Verify JsonManager loads Tasks from existing JSON.
- Input: JsonManager pointing to populated JSON.
- Output: List of Task objects.
- Expected: Tasks list matches JSON content.
- Actual: Tasks loaded successfully. 
**PASS**

### test_json_manager_save_tasks()
- Purpose: Verify JsonManager saves Tasks to JSON.
- Input: JsonManager with Task objects.
- Output: JSON file with Task data.
- Expected: JSON file contains correct Task representation.
- Actual: Tasks saved successfully to JSON. 
**PASS**

## TaskList Tests (src.gui.utils.task_list.TaskList)

### test_task_list_init()
- Purpose: Verify TaskList init links to JsonManager, loads tasks.
- Input: Title string, populated JsonManager.
- Output: TaskList object with title, manager, loaded tasks.
- Expected: TaskList initialized with correct data.
- Actual: Initialized correctly. 
**PASS**

### test_task_list_add_task()
- Purpose: Verify adding task updates list and saves JSON.
- Input: TaskList instance, new Task object.
- Output: Updated TaskList.tasks, updated JSON file.
- Expected: Task appended, list size increases, JSON updated.
- Actual: Task added successfully to list and JSON. 
**PASS**

### test_task_list_delete_task()
- Purpose: Verify deleting task removes from list and saves JSON.
- Input: TaskList instance, title of task to delete.
- Output: Updated TaskList.tasks, updated JSON file.
- Expected: Task removed, list size decreases, JSON updated.
- Actual: Task deleted successfully from list and JSON. 
**PASS**

### test_task_list_get_task()
- Purpose: Verify retrieving task by title.
- Input: TaskList instance, existing/non-existing title.
- Output: Task object or None.
- Expected: Returns Task object if found, else None.
- Actual: Correct Task or None returned. 
**PASS**

### test_task_list_sort_tasks()
- Purpose: Verify tasks list sorting via key function.
- Input: TaskList with tasks, priority sort key function.
- Output: TaskList.tasks list sorted by priority.
- Expected: Internal tasks list reordered by priority.
- Actual: Tasks list sorted correctly. 
**PASS**

### test_task_list_to_dict()
- Purpose: Verify `to_dict` returns correct metadata dictionary.
- Input: TaskList object.
- Output: Dictionary with title and JSON path.
- Expected: Dictionary reflects TaskList metadata.
- Actual: Correct dictionary returned. 
**PASS**

### test_task_list_from_dict()
- Purpose: Verify `from_dict` creates TaskList and loads tasks.
- Input: TaskList metadata dictionary (title, JSON path).
- Output: TaskList object with loaded tasks.
- Expected: TaskList created accurately, tasks loaded.
- Actual: TaskList with tasks created successfully.
**PASS**

## ListJsonManager Tests (src.gui.utils.list_list.ListJsonManager)

### test_list_json_manager_init_new_file()
- Purpose: Verify ListJsonManager init with non-existent master file.
- Input: Path to non-existent master JSON.
- Output: ListJsonManager with correct path, empty lists collection.
- Expected: ListJsonManager initialized, empty lists.
- Actual: Initialized correctly.
**PASS**

### test_list_json_manager_load_lists()
- Purpose: Verify ListJsonManager loads TaskLists from existing master JSON.
- Input: ListJsonManager pointing to populated master JSON.
- Output: List of TaskList objects.
- Expected: Lists collection matches master JSON content.
- Actual: TaskLists loaded successfully.
**PASS**

### test_list_json_manager_save_lists()
- Purpose: Verify ListJsonManager saves TaskList metadata to master JSON.
- Input: ListJsonManager with TaskList objects.
- Output: Master JSON file with TaskList metadata.
- Expected: Master JSON contains correct TaskList metadata.
- Actual: TaskLists saved successfully to master JSON.
**PASS**

## ListList Tests (src.gui.utils.list_list.ListList)

### test_list_list_init()
- Purpose: Verify ListList init links to ListJsonManager, loads TaskLists.
- Input: Populated ListJsonManager.
- Output: ListList object with manager and loaded TaskLists.
- Expected: ListList initialized with correct data.
- Actual: Initialized correctly.
**PASS**

### test_list_list_add_list()
- Purpose: Verify adding TaskList updates collection and saves master JSON.
- Input: ListList instance, new TaskList object.
- Output: Updated ListList.lists, updated master JSON.
- Expected: TaskList appended, size increases, master JSON updated.
- Actual: TaskList added successfully to collection and master JSON.
**PASS**

### test_list_list_delete_list()
- Purpose: Verify deleting TaskList removes from collection and saves master JSON.
- Input: ListList instance, title of TaskList to delete.
- Output: Updated ListList.lists, updated master JSON.
- Expected: TaskList removed, size decreases, master JSON updated.
- Actual: TaskList deleted successfully from collection and master JSON.
**PASS**

### test_list_list_get_list()
- Purpose: Verify retrieving TaskList by title.
- Input: ListList instance, existing/non-existing title.
- Output: TaskList object or None.
- Expected: Returns TaskList object if found, else None.
- Actual: Correct TaskList or None returned.
**PASS**