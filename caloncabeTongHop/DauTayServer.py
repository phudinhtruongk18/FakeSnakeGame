import random


class StrawberryServer:
    def __init__(self, size):
        self.size = size
        self.x = 20 * self.size
        self.y = 5 * self.size

    def move(self):
        self.x = random.randint(1, 38) * self.size
        self.y = random.randint(1, 20) * self.size
        return self.x,self.y
