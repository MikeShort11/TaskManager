
import json

class Task:
    def __init__(self, title: str, date = "no date", time = "no time", description: str = "enter description here", category: str = "no category"):
        """Constructs a new task object with the following data"""
        try:
            assert isinstance(title, str)
            assert isinstance(date, str)  # Change obj type to datetime later
            assert isinstance(time, str)  # Change obj type to datetime later
            assert isinstance(description, str)
            assert isinstance(category, str)
        except AssertionError as err:
            raise TypeError(err)  # Code calling the constructor needs error handling
        else:
            self.title = title
            self.date = date
            self.time = time
            self.description = description
            self.category = category

        #maybe we need this later
    def to_dict(self):
        """Converts task to a dictionary for JSON"""
        return {"title": self.title,
                "date": self.date,
                "time": self.time,
                "description": self.description,
                "category": self.category
            }
    @classmethod
    def from_dict(cls, data):
        """creates a Tasks object from a dictionary"""
        return cls(
            data["title"],
            data["date"],
            data["time"],
            data["description"],
            data["category"]
        )
    def __str__(self):
        return f" {self.title}, {self.date}, {self.time}, {self.description}, {self.category}"

"""task = Task("Meeting")
print(task)"""
