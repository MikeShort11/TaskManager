import task_list

test_list = task_list.TaskList()

def test_add_task():

    test_list.add_task("Test_name")
    assert print(test_list["Test_name"]) == "Test_name"
