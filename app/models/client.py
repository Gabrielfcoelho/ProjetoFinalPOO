from app.models.user import User


class Client(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.admin = 0

    def db_format(self) -> list:
        return [(self.username, self.password, self.admin)]