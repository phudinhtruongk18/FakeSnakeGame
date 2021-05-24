import pickle
import random
import socket
import pygame
from pygame.locals import *
import time


class Snake:
    def __init__(self, parent_screen,background_image, length,color):
        self.imageDuoi = pygame.image.load("duoi.png").convert()
        self.parent_screen = parent_screen
        self.image = pygame.image.load("player.png").convert()
        self.size = self.image.get_size()[0]
        self.direction = 'down'
        self.background_image = background_image

        self.length = length
        self.x = [self.size]*length
        self.y = [self.size]*length
        self.toaDo =[]
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
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

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
        self.image = pygame.image.load("dautaydethuong.png").convert()
        self.size = self.image.get_size()[0]
        self.x = 20 * self.size
        self.y = 5 * self.size

    def draw(self):
        try:
            self.parent_screen.blit(self.image, (self.x, self.y))
        except Exception as e:
            print("chua co du lieu dau tay",e, "du lieu day tay ->",self.x,self.y)

    def move(self,x,y):
        self.x = x
        self.y = y


class AnotherSnake:
    def __init__(self,parent_screen, parent_screen_image, x, y):
        self.parent_screen = parent_screen
        self.parent_screen_image = parent_screen_image
        self.image = pygame.image.load("player2.png").convert()
        self.x = x
        self.y = y
        self.rect = (x, y, 26,26)
        self.size = 26
        self.mau_vitri_another = []

    def draw(self):
        if self.mau_vitri_another is not None:
            print(len(self.mau_vitri_another),"so luong nguoi choi")
            for mauVaToaDo in self.mau_vitri_another:
                try:
                    for index,toaDo in enumerate(mauVaToaDo[1]):
                        if index == 0:
                            self.parent_screen_image.blit(self.image, (toaDo[0],toaDo[1]))
                            continue
                        pygame.draw.rect(self.parent_screen_image, mauVaToaDo[0], pygame.Rect(toaDo[0], toaDo[1], 26, 26))
                except Exception as e:
                    print("None " ,e)

    def set_X_and_Y(self,mausac_va_toado_moi):
        self.mau_vitri_another = mausac_va_toado_moi


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.105.226.101"
        self.port = 6969
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(2048))
            return data
            # tuong ung voi dautayXY (mau sac, vi tri)
        except socket.error as e:
            print(e)
            print("soc")
        except EOFError as f:
            print(f)
            print("Connection Closed")

class Game:
    def __init__(self):
        self.network = Network()

        pygame.init()
        pygame.display.set_caption('Fake Snake Game')

        self.Height = 694
        self.Weight = 1015
        self.running = True
        self.surface = pygame.display.set_mode((self.Weight,self.Height))
        self.surfaceSecond = pygame.display.set_mode((self.Weight,self.Height))
        self.background_image = pygame.image.load("seaBG.jpg").convert()
        self.surface.blit(self.background_image,(0,0))
        self.surface.blit(self.surfaceSecond,(0,0))
        # self.surfaceSecond.blit(self.background_image,(0,0))
        self.snake = Snake(self.surface,self.surfaceSecond, 2,(10,180,255))
        self.snake.draw()
        self.anotherSnake = AnotherSnake(parent_screen=self.surface,parent_screen_image=self.surfaceSecond,
                                         x=20,y=20)
        self.anotherSnake.draw()
        self.strawberry = Strawberry(self.surface)
        self.strawberry.draw()
        if self.strawberry.size == self.snake.size:
            self.size = self.strawberry.size
        else:
            return
        self.level = 0.08

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + self.size:
            if y2 <= y1 < y2 + self.size:
                self.level -= self.level/9
                return True
        return False

    def is_ban_muoi(self, x1, y1):
        if x1 < 0 or y1 < 0 or x1 > self.Weight or y1 > self.Height:
            return True
        else:
            return False

    def display_die(self,num):
        self.display_score()
        font = pygame.font.SysFont('arial',80)
        if num % 2 == 1:
            score2 = font.render(f" Try Again With Space ",True,(238,147,86))
            self.surface.blit(score2,(120,420))

        font = pygame.font.SysFont('arial',300)
        die = font.render("you die",True,(107,58,73))
        self.surface.blit(die,(10,20))
        self.surface.blit(self.surfaceSecond,(0,0))

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Level : {self.snake.length}",True,(255,20,147))
        self.surface.blit(score,(870,10))

    def play(self):
        self.surface.blit(self.background_image,(0,0))
        self.surface.blit(self.surfaceSecond,(0,0))
        self.anotherSnake.draw()
        self.snake.walk()
        self.strawberry.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_ban_muoi(self.snake.x[0], self.snake.y[0]):
            self.running = False

        # if self.is_collision(self.snake.x[0], self.snake.y[0], self.strawberry.x, self.strawberry.y):
        #     self.snake.increase_length()
        #     self.strawberry.move()

    def run(self):
        self.network.getP()
        while self.running:

            dataNhanDuoc = self.network.send(data=[self.snake.color, self.snake.toaDo])
            if dataNhanDuoc is not None:
                dautayXY, toa_do_nguoi_choi_khac = dataNhanDuoc[0],dataNhanDuoc[1]
                self.anotherSnake.set_X_and_Y(toa_do_nguoi_choi_khac)
                self.strawberry.move(dautayXY[0],dautayXY[1])
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_SPACE:
                        self.snake.dash()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    self.running = False

            self.play()
            time.sleep(self.level)

        self.network.send("ENDGAME")
        num = 0
        while not self.running:
            num += 1
            print(num)
            pygame.display.flip()
            self.surface.blit(self.background_image, (0, 0))
            self.display_die(num)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game = Game()
                        game.run()
                elif event.type == QUIT:
                    return
            time.sleep(.1)


if __name__ == '__main__':
    game = Game()
    game.run()
