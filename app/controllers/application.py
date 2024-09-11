from ..models.adm import Adm
from ..models.stock import Stock
from ..models.user import User
from .dataRecord import DataRecord


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

    def register_user(self, username, password, admin=0):
        if admin == 1:
            self.user = Adm(username, password)
        else:
            self.user = User(username, password)
        
        if self.authenticate_user(username, password) is False or admin == 1:
            if isinstance(self.user, Adm):
                self.db.new_admin(self.user)
            else:
                self.db.new_client(self.user)
            return True
        return False
    
    def get_user(self, username, password):
        return self.db.get_user(username, password)
    
    def get_user_by_id(self, user_id):
        return self.db.get_user_by_id(user_id)

    def buy_stock(self, symbol, qtd, price, id):
        newStock = Stock(symbol, qtd, price)
        self.db.add_wallet( newStock, id)
        return

    def sell_stock(self, symbol, qtd, price, id):
        return self.db.rm_wallet(symbol, qtd, price, id)
    
    def get_stock(self, symbol, user_id):
        return self.db.get_stock(symbol, user_id)
    
    def edit_stock(self, symbol, qtd, price, user_id):
        return self.db.edit_stock(symbol, qtd, price, user_id)

    def search_stock(self, symbol, user_id):
        return self.db.get_stock(symbol, user_id)
    
    def delete_stock(self, symbol, user_id):
        return self.db.delete_stock(symbol, user_id)
    
    def delete_record(self, order_id):
        return self.db.delete_record(order_id)

    def get_wallet(self, user_id):
        return self.db.get_wallet(user_id)
    
    def edit_user(self, user_id, username, role, password):
        self.db.edit_user(user_id, username, role, password)
        return
    
    def delete_user(self, user_id):
        self.db.delete_user(user_id)
        return

    def get_users(self):
        return self.db.get_all_users()

    def get_wallets(self):
        return self.db.get_all_wallets()

    def get_records(self):
        return self.db.get_all_records()
