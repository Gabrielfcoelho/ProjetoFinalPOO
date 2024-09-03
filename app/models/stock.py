class Stock():
    def __init__(self, symbol, qtd, price) -> None:
        self.symbol = symbol
        self.price = price
        self.qtd = qtd
        self.cost = price * qtd
 
    def stockData(self):
        self.data = {
            'qtd' : self.qtd,
            'avg_price' : self.price,
            'avg_cost' : self.cost
        }
        return self.data

    def __str__(self) -> str:
        return f"{self.symbol};{self.qtd};{self.price};{self.cost}"
    
    def __add__(self, stock):
        if self.symbol == stock.symbol:
            new_qtd = self.qtd + stock.qtd
            new_price = (self.cost + stock.cost) / new_qtd
            return Stock(self.symbol, new_qtd, new_price)
        return ValueError("Objeto invalido!")