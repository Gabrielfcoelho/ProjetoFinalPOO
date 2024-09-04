from app.models.user import User


class Adm(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.admin = 1

    def db_format(self) -> list:
        return [(self.username, self.password, self.admin)]
