from datetime import date, time

class Task:
    def __init__(self, title: str, date: date, time: time, desc: str, cat: str):
        """Constructs a new task object with the following data-
        self.title: str
        self.date: date
        self.time: time
        self.description: str
        self.category: str
        """
        self.title = title
        self.date = date
        self.time = time
        self.description = desc
        self.category = cat

    def edit_task(self, to_edit: str, input):
        """Edits a task's members based on the incoming data in the arguments.
        Knows what to edit and not to edit.
        Type checks and returns an error message if failed."""
        
        # Type checking
        match to_edit:
            case "date":
                if not isinstance(input, date):
                    return f"Error: input ({input}) does not match to_edit ({to_edit})"
            case "time":
                if not isinstance(input, time):
                    return f"Error: input ({input}) does not match to_edit ({to_edit})"
            case _:
                if not isinstance(input, str):
                    return f"Error: input ({input}) does not match to_edit ({to_edit})"
        
        # Edit the attribute
        match to_edit:
            case "title":
                self.title = input
            case "date":
                self.date = input
            case "time":
                self.time = input
            case "description":
                self.description = input
            case "category":
                self.category = input
            case _:
                return "Error editing case: Unknown Error"
