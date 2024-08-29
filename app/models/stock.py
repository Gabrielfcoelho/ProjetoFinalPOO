class Stock():
    def __init__(self, name, price, qtd) -> None:
        self.name = name
        self.price = price
        self.qtd = qtd

    def __str__(self) -> str:
        return f"{self.name};{self.price};{self.qtd}"