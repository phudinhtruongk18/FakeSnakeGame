import pygame
import random

class Strawberry:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("data/dautaydethuong.png").convert()
        self.size = self.image.get_size()[0]
        self.x = 15 * self.size
        self.y = 15 * self.size

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 25) * self.size
        self.y = random.randint(1, 20) * self.size
