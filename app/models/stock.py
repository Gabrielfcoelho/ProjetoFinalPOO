class Stock():
    def __init__(self, name, price, qtd) -> None:
        self.name = name
        self.price = price
        self.qtd = qtd
        self.cost = self.price * self.qtd
        self.data = {
            'avg_price' : self.price,
            'avg_cost' : self.cost,
            'qtd' : self.qtd
        }

    def __str__(self) -> str:
        return f"{self.name};{self.price};{self.qtd}"