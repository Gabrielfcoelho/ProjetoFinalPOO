class Wallet():
    def __init__(self) -> None:
        self.stock_list = {}

    def buy_stock(self, stock):
        if stock.name not in self.stock_list.keys() :
            self.stock_list[stock.name] = stock.data
        else:
            self.stock_list[stock.name]['qtd'] += stock.qtd
            self.stock_list[stock.name]['avg_cost'] += (stock.qtd * stock.price)
            self.stock_list[stock.name]['avg_price'] = self.stock_list[stock.name]['avg_cost'] / self.stock_list[stock.name]['qtd']

    def sell_stock(self, stock):
        pass