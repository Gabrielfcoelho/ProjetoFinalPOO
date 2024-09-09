import sqlite3
from uuid import uuid4

from ..models.stock import Stock
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
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             username TEXT UNIQUE NOT NULL,
                             password TEXT NOT NULL
                             admin INTEGER DEFAULT 0
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
        if self.cur.execute("SELECT name FROM sqlite_master WHERE name='records'").fetchone() is None:
            self.cur.execute('''CREATE TABLE records(
                             user_id INTEGER,
                             order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                             order_type TEXT NOT NULL,
                             stock TEXT NOT NULL,
                             qtd INTEGER NOT NULL,
                             avg_price REAL NOT NULL,
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
        if self.get_user(self.user.username, self.user.password) is not None:
            self.cur.execute("UPDATE users SET role=1 WHERE username=? AND password=?", (self.user.username, self.user.password))
            self.con.commit()
            return
        self.cur.executemany("INSERT INTO users(username, password, role) VALUES(?, ?, ?)", self.user.db_format())
        self.con.commit()
        return
    
    def get_user(self, username, password):
        self.username = username
        self.password = password
        return self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username, self.password)).fetchone()
    
    def get_user_by_id(self, user_id):
        self.user_id = user_id
        return self.cur.execute("SELECT * FROM users WHERE id=?", (self.user_id,)).fetchone()
    
    def edit_user(self, user_id, username, role, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.cur.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (self.username, self.password, self.role, self.user_id))
        self.con.commit()
        return

    def delete_user(self, user_id):
        self.user_id = user_id
        self.cur.execute("DELETE FROM users WHERE id=?", (self.user_id,))
        self.con.commit()
        return

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
            self.cur. execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(?, ?, ?, ?, ?)", (user_id, 'Compra', newStock.symbol, wallet.stock_list[newStock.symbol].qtd, wallet.stock_list[newStock.symbol].price))
            self.con.commit()
            return
        # adiciona uma nova stock no banco de dados
        self.cur. execute("INSERT INTO wallet Values(?, ?, ?, ?, ?)", (user_id, newStock.symbol, newStock.qtd, newStock.price, newStock.cost))
        self.cur. execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(?, ?, ?, ?, ?)", (user_id, 'Compra', newStock.symbol, newStock.qtd, newStock.price))
        self.con.commit()
        return
    
    # remove stocks para a carteira
    def rm_wallet(self, symbol, qtd, price, user_id):
        if self.cur.execute("SELECT * FROM wallet WHERE stock = ? AND user_id = ?", (symbol, user_id)).fetchone() is not None:
            wallet = Wallet()
            dbSymbol, dbQtd, dbPrice = self.cur.execute("SELECT stock, qtd, avg_price FROM wallet WHERE stock = ? AND user_id = ?", (symbol, user_id)).fetchone()
            # Se a quantidade for menor que a do Banco, retira o número indicado de ações 
            if qtd < dbQtd:
                dbStock = Stock(dbSymbol, dbQtd, dbPrice)
                sellStock = Stock(symbol, qtd, dbPrice)
                wallet.sell_stock(dbStock, sellStock)
                self.cur.execute("UPDATE wallet SET qtd = ?, avg_cost =? WHERE stock = ? AND user_id = ?", (wallet.stock_list[dbSymbol].qtd, wallet.stock_list[dbSymbol].cost, dbSymbol, user_id))
                self.cur. execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(?, ?, ?, ?, ?)", (user_id, 'Venda', symbol, qtd, price))
                self.con.commit()
                return True
            # Se a quantidade for a mesma do Banco, deleta completamente a ação
            elif qtd == dbQtd:
                self.cur.execute("DELETE FROM wallet WHERE stock = ? AND user_id = ?", (dbSymbol, user_id))
                self.cur. execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(?, ?, ?, ?, ?)", (user_id, 'Venda', symbol, qtd, price))
                self.con.commit()
                return True
        else:
            return False
    
    def get_wallet(self, user_id):
        return self.cur.execute("SELECT * FROM wallet WHERE user_id=?", (user_id,)).fetchall()
    
    def get_stock(self, symbol, user_id):
        if self.cur.execute("SELECT * FROM wallet WHERE user_id=? AND stock = ?", (user_id,symbol)).fetchone() is None:
            return False
        return True
    
    def get_records(self, user_id):
        return self.cur.execute("SELECT * FROM records WHERE user_id=?", (user_id,)).fetchall()

    def get_all_users(self):
        return self.cur.execute("SELECT * FROM users").fetchall()
    
    def get_all_wallets(self):
        return self.cur.execute("SELECT * FROM wallet").fetchall()
    
    def get_all_records(self):
        return self.cur.execute("SELECT * FROM records").fetchall()