class Task:
    """Initialize a Task with required title and optional attributes."""
    def __init__(self, title, date="", time="", description="", priority=""):
        self.title = title
        self.date = date
        self.time = time
        self.description = description
        self.priority = priority

    def to_dict(self):
        """Convert the Task object to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "description": self.description,
            "priority": self.priority
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary."""
        return cls(
            title=data["title"],
            date=data.get("date", ""),
            time=data.get("time", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "")
        )


    def __eq__(self, other):
        # Equal comparison (self == other)
        if self.priority == other.category:
            return True
        else:
            return False

    def __ne__(self, other):
        # Not equal comparison (self != other)
        if self.priority == other.category:
            return False
        else:
            return True


    def __lt__(self, other):
        # Less than comparison (self < other)
        if self.priority < other.priority:
            return True
        else:
            return False


    def __le__(self, other):
        # Less than or equal comparison (self <= other)
        if self.priority <= other.priority:
            return True
        else:
            return False


    def __gt__(self, other):
        # Greater than comparison (self > other)
        if self.priority > other.priority:
            return True
        else:
            return False


    def __ge__(self, other):
        # Greater than or equal comparison (self >= other)
        if self.priority >= other.priority:
            return True
        else:
            return False


