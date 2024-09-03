import sqlite3
from uuid import uuid4

from ..models.user import User
from ..models.wallet import Wallet
from ..models.stock import Stock


class DataRecord():

    def __init__(self) -> None:
        self.con = sqlite3.connect('app/controllers/db/site.db')
        self.cur = self.con.cursor()
        self.db_connect()

    def db_connect(self):
        if self.cur.execute("SELECT name from sqlite_master WHERE name='users'").fetchone() is None:
            self.cur.execute('''CREATE TABLE users (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
    def new_client(self, user):
        self.user = user
        self.cur.executemany("INSERT INTO users(username, password) VALUES(?, ?)", self.user.db_format())
        self.con.commit()
        return

    def new_admin(self, user):
        self.user = user
        print("É admin? ", self.user)
        self.cur.executemany("INSERT INTO users(username, password, admin) VALUES(?, ?, ?)", self.user.db_format())
        self.con.commit()
        return
    
    def get_user(self, username, password):
        self.username = username
        self.password = password
        return self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username, self.password)).fetchone()
    
    # adiciona stock para a carteira
    def add_wallet(self, newStock, user_id):
        if self.cur.execute("SELECT * FROM wallet WHERE stock = ? AND user_id = ?", (newStock.symbol, user_id)).fetchone() is not None:
            # instancia wallet
            wallet = Wallet()
            # recupera dados do banco
            name, qtd, price = self.cur.execute("SELECT stock, qtd, avg_price FROM wallet WHERE stock = ? AND user_id = ?", (newStock.symbol, user_id)).fetchone()
            # cria objeto stock com os dados recuperados
            oldStock = Stock(name, qtd, price)
            # soma os dados do novo stock com os armazenados no banco
            wallet.buy_stock(oldStock, newStock)
            # atualiza o banco de dados
            self.cur.execute("UPDATE wallet SET qtd = ?, avg_price = ?, avg_cost = ? WHERE stock = ? AND user_id = ?", (wallet.stock_list[newStock.symbol].qtd,wallet.stock_list[newStock.symbol].price,wallet.stock_list[newStock.symbol].cost, newStock.symbol, user_id))
            self.con.commit()
            return
        # adiciona uma nova stock no banco de dados
        self.cur. execute("INSERT INTO wallet Values(?, ?, ?, ?, ?)", (user_id, newStock.symbol, newStock.qtd, newStock.price, newStock.cost))
        self.con.commit()
        return
    
    # remove stocks para a carteira
    def rm_wallet(self, sellStock, user_id):
        if self.cur.execute("SELECT * FROM wallet WHERE stock = ? AND user_id = ?", (sellStock.symbol, user_id)).fetchone() is not None:
            print("1")
            wallet = Wallet()
            dbSymbol, dbQtd, dbPrice = self.cur.execute("SELECT stock, qtd, avg_price FROM wallet WHERE stock = ? AND user_id = ?", (sellStock.symbol, user_id)).fetchone()
            if sellStock.qtd < dbQtd:
                print("2")
                dbStock = Stock(dbSymbol, dbQtd, dbPrice)
                wallet.sell_stock(dbStock, sellStock)
                print(wallet.stock_list[dbSymbol])
            elif sellStock.qtd == dbQtd:
                self.cur.execute()
        print("3")
