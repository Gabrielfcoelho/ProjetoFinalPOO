# import sqlite3

# from ..models.user import User


# class DataRecord():

#     def __init__(self) -> None:
#         self.con = sqlite3.connect('app/controllers/db/site.db')
#         self.cur = self.con.cursor()
#         self.db_connect()

#     def db_connect(self):
#         if self.cur.execute("SELECT name from sqlite_master WHERE name='users'").fetchone() is None:
#             self.cur.execute("CREATE TABLE users( username, password)")
#         return
        
#     def new_user(self, username, password):
#         self.data = User(username, password)
#         self.cur.executemany("INSERT INTO users VALUES(?, ?)", (self.data.username, self.data.password))
#         self.con.commit()
#         return
    
# def adapter_user(user):
#     return f'{user.username}; {user.password}'
    