import task_list

test_list = task_list()

# test_list.del("example 1") == error

test_list.add("example 1")
# test_list.del("example 1") == empty list

test_list.add("example 2")
test_list.add("example 3")
test_list.add("example 4")
test_list.add("example 5")
# test_list.del("example 4") == list still in proper order with 4 gone.

