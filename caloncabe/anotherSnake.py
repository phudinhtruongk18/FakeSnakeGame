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
        self.mau_vitri_another = []

    def draw(self):
        for mauVaToaDo in self.mau_vitri_another:
            x,y = mauVaToaDo[1][0], mauVaToaDo[1][1]
            pygame.draw.rect(self.parent_screen, mauVaToaDo[0], pygame.Rect(x,y, 26, 26))

    def set_X_and_Y(self,mausac_va_toado_moi):
        self.mau_vitri_another = mausac_va_toado_moi
