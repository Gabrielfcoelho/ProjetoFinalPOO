from app.models.user import User

class Adm(User):
    def __init__(self, username, password):
        super().__init__(username, password)