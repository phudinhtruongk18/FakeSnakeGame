import pygame
from something import IcreamShot, LaserShot


class Boss:
    def __init__(self, parent_screen, x, y,weight_screen,snake):
        self.snake = snake
        self.weight_screen = weight_screen
        self.parent_screen = parent_screen
        self.render_image = pygame.image.load("tainguyen/hinhanh/boss.png")
        self.render_image_360 = pygame.transform.flip(self.render_image, True, False)
        self.size = self.render_image.get_size()[0]
        self.size2 = self.render_image.get_size()[1]
        self.x = x
        self.y = y
        self.count = 0
        self.knifes = []
        self.render_image_temp = self.render_image
        self.huong_dan = "left"
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size2)

    def duoi_theo_nguoi_choi(self):
        if self.y + 26 == self.snake.y[0]:
            print("not tracing")
        elif self.y + 26 < self.snake.y[0]:
            self.y += 7.5
            self.huong_dan = "down"
        else:
            self.y -= 7.5
            self.huong_dan = "up"

        if self.x == self.snake.x[0]:
            print("not tracing")
        elif self.x < self.snake.x[0]:
            self.x += 7.5
            self.render_image_temp = self.render_image_360
            self.huong_dan = "right"
        else:
            self.x -= 7.5
            self.render_image_temp = self.render_image
            self.huong_dan = "left"

        if self.hitbox.colliderect(self.snake.hitbox):
            print("U DIE")

        self.draw()
        self.count += 1
        if self.count > 10:
            self.knifes.append(IcreamShot(self.parent_screen, self.x + 26, self.y + 26, self.huong_dan))
            # self.knifes.append(LaserShot(self.parent_screen, self.x, self.y+52, self.huong_dan))
            self.count = 0

    def draw(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size2)
        pygame.draw.rect(self.parent_screen, (255, 255, 255), self.hitbox, 2)
        for temp_knife in self.knifes:
            if temp_knife.x < 0 or temp_knife.x > self.weight_screen:
                self.knifes.pop(self.knifes.index(temp_knife))
            if temp_knife.xulyhuongdan(self.snake):
                temp_knife.draw()
            else:
                self.knifes.pop(self.knifes.index(temp_knife))

        self.parent_screen.blit(self.render_image_temp, (self.x, self.y))


class Snake:
    def __init__(self, parent_screen, length, color):
        self.imageDuoi = pygame.image.load("tainguyen/hinhanh/duoi.png").convert()
        self.parent_screen = parent_screen
        self.image = pygame.image.load("tainguyen/hinhanh/player.png").convert()
        self.size = self.image.get_size()[0]
        self.direction = 'down'

        self.length = length
        self.x = [self.size] * length
        self.y = [self.size] * length
        self.toaDo = []
        self.hitbox_of_snake = []
        self.color = color

        self.hitbox = pygame.Rect(self.x[0] -5, self.y[0] -5, self.size +10, self.size+10)


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
        self.hitbox_of_snake.clear()
        self.hitbox = pygame.Rect(self.x[0] -5, self.y[0] -5, self.size +10, self.size+10)
        pygame.draw.rect(self.parent_screen, (255, 255, 255), self.hitbox, 2)

        for i in range(self.length):
            hitbox = (self.x[i] - 5, self.y[i] - 5, self.size + 10, self.size + 10)
            pygame.draw.rect(self.parent_screen, (0, 255, 255), hitbox, 2)

            self.hitbox_of_snake.append(hitbox)
            self.toaDo.append((self.x[i], self.y[i]))
            if i == 0:
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.imageDuoi, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def decrease_length(self):
        self.length -= 1
        self.x.append(+1)
        self.y.append(+1)


class Strawberry:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.images = [pygame.image.load("tainguyen/hinhanh/dautay1.png"), pygame.image.load(
            "tainguyen/hinhanh/dautay2.png"),
                       pygame.image.load("tainguyen/hinhanh/dautay3.png"), pygame.image.load(
                "tainguyen/hinhanh/dautay4.png"),
                       pygame.image.load("tainguyen/hinhanh/dautay5.png")]
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
        self.image = pygame.image.load("tainguyen/hinhanh/player2.png").convert()
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

