from models import ToDoModel

# Service.py
class ToDoService:
    def __init__(self):
        self.model = ToDoModel()

    def create(self, params):
        text = params.get("Title")
        description = params.get("Description")
        return self.model.create(text,description)

    def list(self):
        response = self.model.list_items()
        return response
