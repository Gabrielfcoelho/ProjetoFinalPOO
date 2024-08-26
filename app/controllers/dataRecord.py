import sqlite3

from ..models.user import User


class DataRecord():

    def __init__(self) -> None:
        self.con = sqlite3.connect('app/controllers/db/site.db')
        self.cur = self.con.cursor()
        self.db_connect()

    def db_connect(self):
        if self.cur.execute("SELECT name from sqlite_master WHERE name='users'").fetchone() is None:
            self.cur.execute("CREATE TABLE users( username, password)")
        return
        
    def new_user(self, user):
        self.user = user
        self.cur.executemany("INSERT INTO users VALUES(?, ?)", self.user.db_format())
        self.con.commit()
        return
    