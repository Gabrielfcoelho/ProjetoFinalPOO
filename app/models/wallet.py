class Wallet():
    def __init__(self) -> None:
        self.stock_list = {}

    def buy_stock(self, stock01, stock02):
        if stock01.symbol == stock02.symbol:
            self.stock_list[stock01.symbol] = stock01 + stock02

    def sell_stock(self, stock):
        if stock.symbol not in self.stock_list.keys():
            return
        self.stock_list[stock.symbol] -= stock