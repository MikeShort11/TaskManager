# Test Artifacts - Milestone 2

## test_main.py

### test_help_menu()
- Tests if the help menu quits properly.
- Input: "" (an empty string)
- Output: None
- Expected Results: Triggers the user's return to the CLI's main menu
- Actual Results: Successfully returns the user back to main menu
**PASS**

## test_task.py

### test_create_task()
- Test if task construction works as intended at the class level. 
- Inputs: "task1"
- Outputs: "task1" "no date" "no time" "enter description here" "no category"
- Expected Results: creates a task with the inputted name and default values
- Actual Results: All values in the task object are correct.
**PASS**

### test_str()
- Tests if the __str__ magic method works properly for the task object.
- Input: "task1"
- Output: " task1, no date, no time, enter description here, no category"
- Expected Results: prints the values of the task object
- Actual Results: Task object successfully prints values
**PASS**

## test_task_list.py

### test_add_task()
- Tests if the add function actually adds the task properly. Checks if size of list is accurate.
- Input: "task1"
- Output: "task1 task added successfully."
- Expected Results: A new task object is added to the task_list object.
- Actual Results: Task object successfully created and added to task_list.
**PASS**

### test_add_duplicate_task()
- Function should return early if task name is already in use.
- Input: "task1"
- Output: "'task1' is taken, try another name."
- Expected Results: Rejects the use of the task name, the task name must be unique.
- Actual Results: Adding a task with a duplicate name gets rejected.
**PASS**

### test_delete()
- Tests for expected behavior of successful task deletion. 
- Input: delete("task1") add("task2") add("task3") add ("task4") add("task5") delete("task4")
- Output: "task1 deleted" "task2, task 3, task5"
- Expected Results: Deletes task 1, adds task 2,3,4,5, deletes task 4, prints task 2,3,4
- Actual Results: Deletions are successful.
**PASS**

### test_delete_missing()
- Tests for proper behavior from delete if the task isn't found. 
- Input: "task1"
- Output: "Key not found!"
- Expected Results: Deleting a task that doesn't exist is rejected with a message.
- Actual Results: Correct message found.
**PASS**
