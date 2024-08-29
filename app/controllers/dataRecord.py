import sqlite3
from uuid import uuid4
from ..models.user import User
from ..models.wallet import Wallet


class DataRecord():

    def __init__(self) -> None:
        self.con = sqlite3.connect('app/controllers/db/site.db')
        self.cur = self.con.cursor()
        self.db_connect()

    def db_connect(self):
        if self.cur.execute("SELECT name from sqlite_master WHERE name='users'").fetchone() is None:
            self.cur.execute('''CREATE TABLE users (
                             username TEXT UNIQUE NOT NULL,
                             password TEXT NOT NULL
                             )
                             ''')
        if self.cur.execute("SELECT name from sqlite_master WHERE name='wallet'").fetchone() is None:
            self.cur.execute('''CREATE TABLE wallet (
                             user_id INTEGER,
                             stock TEXT NOT NULL,
                             qtd INTEGER NOT NULL,
                             avg_price REAL NOT NULL,
                             avg_cost REAL NOT NULL,
                             FOREIGN KEY (user_id) REFERENCES users(id)
                             )
                             ''')
        return
        
    def new_user(self, user):
        self.user = user
        self.cur.executemany("INSERT INTO users VALUES(?, ?)", self.user.db_format())
        self.con.commit()
        return

    def get_user(self, username, password):
        self.username = username
        self.password = password
        return self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username, self.password)).fetchone()
    
    #testanto update da carteira
    def update_wallet(self, stock):
        self.stock = stock
        self.wallet = Wallet()
        self.wallet.add_stock(stock)
        self.cur.executemany("INSERT INTO wallet VALUES(?, ?, ?, ?, ?)", 
                             [
                                 (
                                    self.stock.name,
                                    self.wallet.stock_list[stock.name]['qtd'], 
                                    self.wallet.stock_list[stock.name]['avg_price'], 
                                    self.wallet.stock_list[stock.name]['avg_cost']
                                    )
                                ]
                             )
        self.con.commit()
        return
    
    #testando carteira
    def show_wallet(self):
        return self.cur.execute("SELECT * FROM wallet WHERE stock='BBAS3F'").fetchall()
    
