import pygame


class LaserShot:
    def __init__(self,parent_screen, x, y, huong_dan):
        self.y = y
        self.x = x
        self.image = pygame.image.load("tainguyen/hinhanh/laser.png")
        self.imageXoay = pygame.transform.rotate(self.image, 90)
        self.parent_screen = parent_screen
        chieu_ban,self.huong_dan = self.tim_huong_laser(huong_dan)
        self.vel = 20 * chieu_ban
        self.facing = chieu_ban
        pygame.mixer.Sound("tainguyen/amthanh/lasersound.wav").play()

    def xulyhuongdan(self):
        if self.huong_dan:
            self.x += self.vel
        else:
            self.y += self.vel

    def draw(self):
        if self.huong_dan:
            for temp in range(40):
                self.parent_screen.blit(self.image, (self.x+temp*26*self.facing, self.y))
        else:
            for temp in range(40):
                self.parent_screen.blit(self.imageXoay, (self.x, self.y+temp*26*self.facing))

    def tim_huong_laser(self, huong):
        switcher = {
            "left": [-1,True],
            "right": [1,True],
            "up": [-1,False],
            "down": [1,False]
        }
        return switcher.get(huong, "Invalid huong di of week")

