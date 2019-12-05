from random import choice
from string import ascii_letters, digits


class Team:
    def __init__(self, name):
        self.name = name
        self.token = self.gen_token()

    def gen_token(self):
        return ''.join(choice(ascii_letters + digits) for _ in range(16))

    def dict_(self):
        return {"name": self.name, "token": self.token}
