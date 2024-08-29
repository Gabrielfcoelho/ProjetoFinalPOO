class Wallet():
    def __init__(self) -> None:
        self.stock_list = {}

    def add_stock(self, stock):
        if stock.name is not self.stock_list.keys():
            self.stock_list.update({stock.name : {'avg_price' : stock.price,
                                                'avg_cost' : stock.price,
                                                'qtd' : stock.qtd}})
            print(type(stock.name))
            print(type(stock.price))
            print(type(stock.qtd))
        self.stock_list[stock.name]['qtd'] += stock.qtd
        self.stock_list[stock.name]['avg_cost'] += (stock.qtd * stock.price)
        self.stock_list[stock.name]['avg_price'] = self.stock_list[stock.name]['avg_cost'] / self.stock_list[stock.name]['qtd']