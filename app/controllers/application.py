from .dataRecord import DataRecord
from ..models.user import User

class Application():

    def __init__(self):
        self.pages = {}
        self.db = DataRecord()

    def authenticate_user(self, username, password):
        self.username = username
        self.password = password
        if self.db.get_user(self.username, self.password) is None:
            return False
        return True

    def register_user(self, username, password):
        self.user = User(username, password)
        if self.authenticate_user(username, password) == False:
            self.db.new_user(self.user)
            return True
        return False
