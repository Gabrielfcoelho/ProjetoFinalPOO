class Wallet():
    def __init__(self) -> None:
        self.stock_list = {}

    def buy_stock(self, dbStock, newStock):
        if dbStock.symbol == newStock.symbol:
            self.stock_list[dbStock.symbol] = dbStock + newStock
        return

    def sell_stock(self, dbStock, sellStock):
        self.stock_list[dbStock.symbol] = dbStock - sellStock
        return