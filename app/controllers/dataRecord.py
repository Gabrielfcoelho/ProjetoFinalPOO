import os

import psycopg2

from ..models.stock import Stock
from ..models.wallet import Wallet


class DataRecord():

    def __init__(self) -> None:
        self.con = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'my_database'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
            host=os.getenv('POSTGRES_HOST', 'db'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        self.cur = self.con.cursor()
        self.db_connect()

    def db_connect(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role INTEGER DEFAULT 0
            );
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS wallet (
                user_id INTEGER,
                stock TEXT NOT NULL,
                qtd INTEGER NOT NULL,
                avg_price REAL NOT NULL,
                avg_cost REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                user_id INTEGER,
                order_id SERIAL PRIMARY KEY,
                order_type TEXT NOT NULL,
                stock TEXT NOT NULL,
                qtd INTEGER NOT NULL,
                avg_price REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        self.con.commit()
        return
        
    def new_client(self, user):
        self.user = user
        self.cur.executemany("INSERT INTO users(username, password) VALUES(%s, %s)", self.user.db_format())
        self.con.commit()
        return

    def new_admin(self, user):
        self.user = user
        if self.get_user(self.user.username, self.user.password) is not None:
            self.cur.execute("UPDATE users SET role=1 WHERE username=%s AND password=%s", (self.user.username, self.user.password))
            self.con.commit()
            return
        self.cur.executemany("INSERT INTO users(username, password, role) VALUES(%s, %s, %s)", self.user.db_format())
        self.con.commit()
        return
    
    def get_user(self, username, password):
        self.username = username
        self.password = password
        self.cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        return self.cur.fetchone()

    def get_user_by_id(self, user_id):
        self.user_id = user_id
        self.cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        return self.cur.fetchone()
    
    def edit_user(self, user_id, username, role, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.cur.execute("UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s", (self.username, self.password, self.role, self.user_id))
        self.con.commit()
        return

    def delete_user(self, user_id):
        self.user_id = user_id
        self.cur.execute("DELETE FROM records WHERE user_id=%s", (self.user_id,))
        self.cur.execute("DELETE FROM wallet WHERE user_id=%s", (self.user_id,))
        self.cur.execute("DELETE FROM users WHERE id=%s", (self.user_id,))
        self.con.commit()
        return

    # adiciona stock para a carteira
    def add_wallet(self, newStock, user_id):
        self.cur.execute("SELECT * FROM wallet WHERE user_id = %s AND stock=%s", (user_id, newStock.symbol))
        if self.cur.fetchone() is not None:
            # instancia wallet
            wallet = Wallet()
            # recupera dados do banco
            self.cur.execute("SELECT stock, qtd, avg_price FROM wallet WHERE user_id = %s", (user_id,))
            name, qtd, price = self.cur.fetchone()
            # cria objeto stock com os dados recuperados
            oldStock = Stock(name, qtd, price)
            # soma os dados do novo stock com os armazenados no banco
            wallet.buy_stock(oldStock, newStock)
            # atualiza o banco de dados
            self.cur.execute("UPDATE wallet SET qtd = %s, avg_price = %s, avg_cost = %s WHERE stock = %s AND user_id = %s", (wallet.stock_list[newStock.symbol].qtd,wallet.stock_list[newStock.symbol].price,wallet.stock_list[newStock.symbol].cost, newStock.symbol, user_id))
            self.cur.execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(%s, %s, %s, %s, %s)", (user_id, 'Compra', newStock.symbol, wallet.stock_list[newStock.symbol].qtd, wallet.stock_list[newStock.symbol].price))
            self.con.commit()
            return
        # adiciona uma nova stock no banco de dados
        self.cur. execute("INSERT INTO wallet Values(%s, %s, %s, %s, %s)", (user_id, newStock.symbol, newStock.qtd, newStock.price, newStock.cost))
        self.cur. execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(%s, %s, %s, %s, %s)", (user_id, 'Compra', newStock.symbol, newStock.qtd, newStock.price))
        self.con.commit()
        return
    
    # remove stocks para a carteira
    def rm_wallet(self, symbol, qtd, price, user_id):
        self.cur.execute("SELECT * FROM wallet WHERE stock = %s AND user_id = %s", (symbol, user_id))
        if self.cur.fetchone() is not None:
            wallet = Wallet()
            self.cur.execute("SELECT stock, qtd, avg_price FROM wallet WHERE stock = %s AND user_id = %s", (symbol, user_id))
            dbSymbol, dbQtd, dbPrice = self.cur.fetchone()
            # Se a quantidade for menor que a do Banco, retira o número indicado de ações 
            if qtd < dbQtd:
                dbStock = Stock(dbSymbol, dbQtd, dbPrice)
                sellStock = Stock(symbol, qtd, dbPrice)
                wallet.sell_stock(dbStock, sellStock)
                self.cur.execute("UPDATE wallet SET qtd = %s, avg_cost =%s WHERE stock = %s AND user_id = %s", (wallet.stock_list[dbSymbol].qtd, wallet.stock_list[dbSymbol].cost, dbSymbol, user_id))
                self.cur.execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(%s, %s, %s, %s, %s)", (user_id, 'Venda', symbol, qtd, price))
                self.con.commit()
                return True
            # Se a quantidade for a mesma do Banco, deleta completamente a ação
            elif qtd == dbQtd:
                self.cur.execute("DELETE FROM wallet WHERE stock = %s AND user_id = %s", (dbSymbol, user_id))
                self.cur.execute("INSERT INTO records(user_id, order_type, stock, qtd, avg_price) Values(%s, %s, %s, %s, %s)", (user_id, 'Venda', symbol, qtd, price))
                self.con.commit()
                return True
        else:
            return False
    
    def get_wallet(self, user_id):
        self.cur.execute("SELECT * FROM wallet WHERE user_id=%s", (user_id,))
        return self.cur.fetchall()

    def edit_stock(self, symbol, qtd, price, user_id):
        self.cur.execute("UPDATE wallet SET qtd = %s, avg_price = %s, avg_cost = %s WHERE stock = %s AND user_id = %s", (qtd, price, f"{(float(qtd)*float(price)):.2f}", symbol, user_id))
        self.con.commit()
        return

    def delete_stock(self, symbol, user_id):
        self.cur.execute("DELETE FROM wallet WHERE stock = %s AND user_id = %s", (symbol, user_id))
        self.con.commit()
        return
    
    def delete_record(self, order_id):
        self.cur.execute("DELETE FROM records WHERE order_id = %s", (order_id,))
        self.con.commit()
        return
    
    def get_stock(self, symbol, user_id):
        self.cur.execute("SELECT * FROM wallet WHERE user_id=%s AND stock = %s", (user_id,symbol))
        return self.cur.fetchone()

    def get_records(self, user_id):
        self.cur.execute("SELECT * FROM records WHERE user_id=%s", (user_id,))
        return self.cur.fetchall()

    def get_all_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def get_all_wallets(self):
        self.cur.execute("SELECT * FROM wallet")
        return self.cur.fetchall()

    def get_all_records(self):
        self.cur.execute("SELECT * FROM records")
        return self.cur.fetchall()