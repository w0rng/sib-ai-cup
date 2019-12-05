from random import randint, choice
from string import ascii_letters, digits


class Bot:
    def __init__(self, name):
        self.name = name
        self.token = self.gen_token()
        self.color = self.gen_color()
        self.coord = self.gen_coords()

    def gen_coords(self):
        return (
            randint(126, 256),
            randint(126, 256),
            randint(126, 256)
        )

    def gen_color(self):
        return {
            'x': randint(0, 2048),
            'y': randint(0, 2048)
        }

    def gen_token(self):
        return ''.join(choice(ascii_letters + digits) for _ in range(16))

    def dict_(self):
        return {
            'name': self.name,
            'token': self.token,
            'color': self.color,
            'coords': self.coord
        }
