import pygame


class IcreamShot:
    def __init__(self, parent_screen, x, y, huong_dan):
        self.y = y
        self.x = x
        animate1 = pygame.transform.scale(pygame.image.load("tainguyen/hinhanh/icream.png"), (52, 52))
        animate2 = pygame.transform.scale(pygame.image.load("tainguyen/hinhanh/icream2.png"), (52, 52))
        animate3 = pygame.transform.scale(pygame.image.load("tainguyen/hinhanh/icream3.png"), (52, 52))
        self.parent_screen = parent_screen
        chieu_ban, self.huong_dan = self.tim_huong_laser(huong_dan)

        if chieu_ban < 0:
            self.images = [animate1, animate2, animate3]
        else:
            self.images = [pygame.transform.flip(animate1, True, False),
                           pygame.transform.flip(animate2, True, False),
                           pygame.transform.flip(animate3, True, False)]

        self.vel = 20 * chieu_ban
        self.facing = chieu_ban
        pygame.mixer.Sound("tainguyen/amthanh/knife.wav").play()
        self.count = 0

    def xulyhuongdan(self):
        if self.huong_dan:
            self.x += self.vel
        else:
            self.y += self.vel

    def draw(self):
        # if self.count % 2 == 0:
        self.parent_screen.blit(self.images[self.count], (self.x + 26 * self.facing, self.y))
        self.count += 1
        if self.count == 2:
            self.count = 0

    def tim_huong_laser(self, huong):
        switcher = {
            "left": [-1, True],
            "right": [1, True],
            "up": [-1, False],
            "down": [1, False]
        }
        return switcher.get(huong, "Invalid huong di")


class LaserShot:
    def __init__(self, parent_screen, x, y, huong_dan):
        self.y = y
        self.x = x
        self.image = pygame.image.load("tainguyen/hinhanh/laser.png")
        self.imageXoay = pygame.transform.rotate(self.image, 90)
        self.parent_screen = parent_screen
        chieu_ban, self.huong_dan = self.tim_huong_laser(huong_dan)
        self.vel = 20 * chieu_ban
        self.facing = chieu_ban
        pygame.mixer.Sound("tainguyen/amthanh/lasersound.wav").play()
        self.is_show = True
        self.show_time = 3

    def xulyhuongdan(self):
        if self.huong_dan:
            self.x += self.vel
        else:
            self.y += self.vel
        self.show_time -= 1
        if self.show_time == 0:
            self.is_show = False

    def draw(self):
        if self.huong_dan:
            for temp in range(40):
                self.parent_screen.blit(self.image, (self.x + temp * 26 * self.facing, self.y))
        else:
            for temp in range(40):
                self.parent_screen.blit(self.imageXoay, (self.x, self.y + temp * 26 * self.facing))

    def tim_huong_laser(self, huong):
        switcher = {
            "left": [-1, True],
            "right": [1, True],
            "up": [-1, False],
            "down": [1, False]
        }
        return switcher.get(huong, "Invalid huong di")
