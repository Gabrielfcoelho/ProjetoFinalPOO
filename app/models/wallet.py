class Wallet():
    def __init__(self) -> None:
        self.stock_list = {}

    def buy_stock(self, stock):
        if stock.symbol not in self.stock_list.keys() :
            self.stock_list[stock.symbol] = stock.data
        else:
            self.stock_list[stock.symbol]['qtd'] += stock.qtd
            self.stock_list[stock.symbol]['avg_cost'] += (stock.qtd * stock.price)
            self.stock_list[stock.symbol]['avg_price'] = self.stock_list[stock.symbol]['avg_cost'] / self.stock_list[stock.symbol]['qtd']

    def sell_stock(self, stock):
        if stock.symbol not in self.stock_list.keys():
            return
        self.stock_list[stock.symbol]['qtd'] -= stock.qtd
        self.stock_list[stock.symbol]['avg_cost'] -= (stock.qtd * stock.price)
        self.stock_list[stock.symbol]['avg_price'] = self.stock_list[stock.symbol]['avg_cost'] / self.stock_list[stock.symbol]['qtd']
