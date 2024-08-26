import sqlite3


class User():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.con = sqlite3.connect('app/controllers/db/site.db')
        self.cur = self.con.cursor()
        self.db_connect()

    def db_connect(self):
        if self.cur.execute("SELECT name from sqlite_master WHERE name='users'").fetchone() is None:
            self.cur.execute("CREATE TABLE users( username, password)")
        return

    def __repr__(self) -> str:
        return f'{self.username}; {self.password}'
    
    def register(self):
        self.cur.execute("INSERT INTO users VALUES(?, ?)", (self.username, self.password))
        self.con.commit()
        return 200