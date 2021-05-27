import pygame


class Snake:
    def __init__(self, parent_screen, background_image, length, color):
        self.imageDuoi = pygame.image.load("tainguyen/duoi.png").convert()
        self.parent_screen = parent_screen
        self.image = pygame.image.load("tainguyen/player.png").convert()
        self.size = self.image.get_size()[0]
        self.direction = 'down'
        self.background_image = background_image

        self.length = length
        self.x = [self.size] * length
        self.y = [self.size] * length
        self.toaDo = []
        self.color = color

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def dash(self):
        self.walk()
        self.walk()
        self.walk()
        self.walk()

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= self.size
        if self.direction == 'right':
            self.x[0] += self.size
        if self.direction == 'up':
            self.y[0] -= self.size
        if self.direction == 'down':
            self.y[0] += self.size

        self.draw()

    def draw(self):
        self.toaDo.clear()
        for i in range(self.length):
            self.toaDo.append((self.x[i], self.y[i]))
            if i == 0:
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.imageDuoi, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Strawberry:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.images = [pygame.image.load("tainguyen/dautay1.png"),pygame.image.load("tainguyen/dautay2.png"),
                      pygame.image.load("tainguyen/dautay3.png"),pygame.image.load("tainguyen/dautay4.png"),
                      pygame.image.load("tainguyen/dautay5.png")]
        # self.size = self.image.get_size()[0]
        self.size = 26
        self.x = 20 * self.size
        self.y = 5 * self.size
        self.count = 0
        self.animation = 0

    def draw(self):
        try:
            self.count += 1
            self.parent_screen.blit(self.images[self.animation], (self.x, self.y))
            if self.count == 7:
                self.animation += 1
                if self.animation == 4:
                    self.animation = 0
                self.count = 0
        except Exception as e:
            print("chua co du lieu dau tay", e, "du lieu day tay ->", self.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y

class AnotherSnake:
    def __init__(self, parent_screen, parent_screen_image, x, y):
        self.parent_screen = parent_screen
        self.parent_screen_image = parent_screen_image
        self.image = pygame.image.load("tainguyen/player2.png").convert()
        self.x = x
        self.y = y
        self.rect = (x, y, 26, 26)
        self.size = 26
        self.mau_vitri_another = []

    def draw(self):
        if self.mau_vitri_another is not None:
            print(len(self.mau_vitri_another), "so luong nguoi choi")
            for indexmau, mauVaToaDo in enumerate(self.mau_vitri_another):
                try:
                    for index, toaDo in enumerate(mauVaToaDo[1]):
                        if index == 0:
                            self.parent_screen_image.blit(self.image, (toaDo[0], toaDo[1]))
                            continue
                        pygame.draw.rect(self.parent_screen_image, mauVaToaDo[0],
                                         pygame.Rect(toaDo[0], toaDo[1], 26, 26))
                except Exception as e:
                    print("None ", e, indexmau)

    def set_X_and_Y(self, mausac_va_toado_moi):
        self.mau_vitri_another = mausac_va_toado_moi
