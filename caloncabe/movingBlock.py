import pygame
from pygame.locals import *
import time
from network import Network
from snake import Snake
from strawberry import Strawberry
from anotherSnake import AnotherSnake

class Game:
    def __init__(self):
        self.network = Network()

        pygame.init()

        # self.surface = pygame.display.set_mode((1000, 800))
        self.Height = 694
        self.Weight = 1015
        self.running = True
        self.surface = pygame.display.set_mode((self.Weight,self.Height))
        self.background_image = pygame.image.load("data/seaBG.jpg").convert()
        self.surface.blit(self.background_image,(0,0))
        self.snake = Snake(self.surface,self.background_image, 2)
        self.snake.draw()
        self.anotherSnake = AnotherSnake(parent_screen=self.surface,parent_screen_image=self.background_image,x=20,y=20,color=(255,255,255))
        self.anotherSnake.draw()
        self.strawberry = Strawberry(self.surface)
        self.strawberry.draw()
        if self.strawberry.size == self.snake.size:
            self.size = self.strawberry.size
        else:
            return
        self.level = 0.1

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

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Level : {self.snake.length}",True,(255,20,147))
        self.surface.blit(score,(870,10))

    def play(self):

        self.surface.blit(self.background_image,(0,0))
        self.snake.walk()
        self.strawberry.draw()
        self.anotherSnake.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_ban_muoi(self.snake.x[0], self.snake.y[0]):
            self.running = False
        # pygame.display.update()

        # pygame.display.flip()
        print(self.snake.x[0], self.snake.y[0], self.strawberry.x, self.strawberry.y)
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.strawberry.x, self.strawberry.y):
            self.snake.increase_length()
            self.strawberry.move()

    def run(self):
        self.network.getP()
        while self.running:
            self.anotherSnake.set_X_and_Y(self.network.send(data=[self.snake.x[0], self.snake.y[0]]))
            print("nhan 2",self.network.getP())
            print("nhan",self.anotherSnake.x,self.anotherSnake.y)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    if event.key == K_LEFT:
                        self.snake.move_left()

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
