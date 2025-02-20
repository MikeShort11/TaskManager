import datetime
import json

class Task:
    def __init__(
            self,
            title: str,
            date=0,
            time=0,
            description: str = "enter description here",
            category: str = "no category"
    ):
        """Constructs a new task object with the following data"""
        self.title = title
        if isinstance(date, int):
            self.date = "no date"
        else:
            self.date = self.parse_date(date) #converts date str into date time

        if isinstance(time, int):
            self.time = "no time"
        else:
            self.time = self.parse_time(time) #converts time str into date time

        self.description = description
        self.category = category
    def parse_date(self, date_str):
        # converts date str into date time
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("invalid date formate. try YYYY-MM-DD")
    def parse_time(self, time_str):
        # converts time str into date time
        try:
            return datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            raise ValueError("invalid time formate. try HH:MM")



    def to_dict(self):
        """Converts task to a dictionary for JSON"""
        return {"title": self.title,
                "date": self.date.strftime('%Y-%m-%d') if isinstance(self.date, datetime.date) else "no date",
                "time": self.date.strftime('%H:%M') if isinstance(self.time, datetime.time) else "no time",
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
