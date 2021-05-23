import pygame


class AnotherSnake:
    def __init__(self,parent_screen, parent_screen_image, x, y,color):
        self.parent_screen = parent_screen
        self.parent_screen_image = parent_screen_image
        self.color = color
        self.x = x
        self.y = y
        self.rect = (x, y, 26,26)
        self.size = 26

    def draw(self):
        pygame.draw.rect(self.parent_screen, self.color, self.rect)

    def set_X_and_Y(self,toa_do):
        self.x = toa_do[0]
        self.y = toa_do[1]
        self.rect = (self.x, self.y, 26,26)
