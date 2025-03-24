class Task:
    """Initialize a Task with required title and optional attributes."""
    def __init__(self, title, date="", time="", description="", category=""):
        self.title = title
        self.date = date
        self.time = time
        self.description = description
        self.category = category

    def to_dict(self):
        """Convert the Task object to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "description": self.description,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary."""
        return cls(
            title=data["title"],
            date=data.get("date", ""),
            time=data.get("time", ""),
            description=data.get("description", ""),
            category=data.get("category", "")
        )