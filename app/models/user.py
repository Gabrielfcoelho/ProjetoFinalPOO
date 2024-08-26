import sqlite3


class User():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def db_format(self) -> list:
        return [(self.username, self.password)]