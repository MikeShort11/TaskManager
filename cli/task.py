from datetime import datetime

class Task:
    def __init__(self,title:str,date:str,time:str,description:str,catagory:str):
        """Constructs a new task object with the following data-"""
        self.title = title
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.time = datetime.strptime(time, '%H:%M').time()
        self.description = description
        self.category = catagory


    def edit_task (self, arg1, arg2, arg_etc):
        """Edits a task's members based on the incoming data in the arguments.
        Knows what to edit and not to edit.
        Type checks and returns an error message if failed."""
        pass
task = Task("Meeting", "2025-02-16", "14:30", "Discuss project updates", "Work")
print(task)