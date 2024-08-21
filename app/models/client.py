from app.models.user import User

class Client(User):
    def __init__(self, username, password):
        super().__init__(username, password)