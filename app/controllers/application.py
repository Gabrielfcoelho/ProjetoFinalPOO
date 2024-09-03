from flask_session import Session

from ..models.adm import Adm
from ..models.stock import Stock
from ..models.user import User
from ..models.wallet import Wallet
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

    def buy_stock(self, symbol, qtd, price, id):
        newStock = Stock(symbol, qtd, price)
        self.db.update_wallet( newStock, id)
        return