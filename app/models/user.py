from .wallet import Wallet


class User():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.wallet = Wallet()

    def db_format(self) -> list:
        return [(self.username, self.password)]