import pygame
from pygame.locals import *
import time
from caloncabe.network import Network
from snake import Snake
from strawberry import Strawberry


class Game:
    def __init__(self):
        self.network = Network()

        pygame.init()

        # self.surface = pygame.display.set_mode((1000, 800))
        self.Height = 629
        self.Weight = 1100
        self.running = True
        self.surface = pygame.display.set_mode((self.Weight,self.Height))
        self.background_image = pygame.image.load("data/seaBG.png").convert()
        self.surface.blit(self.background_image,(0,0))
        self.snake = Snake(self.surface,self.background_image, 2)
        self.snake.draw()
        self.strawberry = Strawberry(self.surface)
        self.strawberry.draw()
        if self.strawberry.size == self.snake.size:
            self.size = self.strawberry.size
        else:
            return
        self.level = 0.3

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
            score2 = font.render(f" Try Again With Space ",True,(255,255,0))
            self.surface.blit(score2,(120,420))

        font = pygame.font.SysFont('arial',300)
        die = font.render("you die",True,(255,0,0))
        self.surface.blit(die,(10,20))
        print(self.network.send("aaa"))

    def display_score(self):
        font = pygame.font.SysFont('arial',60)
        score = font.render(f"Level : {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def play(self):
        self.snake.walk()
        self.strawberry.draw()
        if self.is_ban_muoi(self.snake.x[0], self.snake.y[0]):
            self.running = False
        else:
            self.display_score()

        pygame.display.flip()
        print(self.snake.x[0], self.snake.y[0], self.strawberry.x, self.strawberry.y)
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.strawberry.x, self.strawberry.y):
            self.snake.increase_length()
            self.strawberry.move()

    def run(self):
        self.network.getP()
        while self.running:
            print(self.network.send("aaa"))
            print(self.network.getP())
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
            time.sleep(.5)


if __name__ == '__main__':
    game = Game()
    game.run()
