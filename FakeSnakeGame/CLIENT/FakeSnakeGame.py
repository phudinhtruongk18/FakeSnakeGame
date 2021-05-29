import pickle
import pygame
from pygame.locals import *
from textInput import TextInputBox
from network import Network
from character import Snake, Strawberry, AnotherSnake, Boss
from something import LaserShot


class Game:
    def __init__(self):
        self.network = Network()

        pygame.init()
        pygame.display.set_caption('Fake Snake Game')
        self.clock = pygame.time.Clock()
        self.Height = 694
        self.Weight = 1015
        self.running = True
        self.surface = pygame.display.set_mode((self.Weight, self.Height))
        self.surfaceSecond = pygame.display.set_mode((self.Weight, self.Height))
        self.background_image = pygame.image.load("tainguyen/hinhanh/seaBG.png").convert()
        self.surface.blit(self.background_image, (0, 0))
        self.surface.blit(self.surfaceSecond, (0, 0))
        # self.surfaceSecond.blit(self.background_image,(0,0))
        self.snake = Snake(self.surfaceSecond, 2, "#5404CA")
        self.snake.draw()
        self.anotherSnake = AnotherSnake(parent_screen=self.surface, parent_screen_image=self.surfaceSecond,
                                         x=20, y=20)
        self.anotherSnake.draw()
        self.strawberry = Strawberry(self.surface)
        self.anggryDauTay = Boss(self.surface,26,52)
        self.strawberry.draw()
        self.anggryDauTay.draw()
        if self.strawberry.size == self.snake.size:
            self.size = self.strawberry.size
        else:
            return
        self.level = 5
        self.playerName = "No Name"
        self.eatSound = pygame.mixer.Sound("tainguyen/amthanh/eat.wav")
        self.zoGameSound = pygame.mixer.Sound("tainguyen/amthanh/heheboiz.wav")
        self.sieunangluc = []

    def is_ban_muoi(self, x1, y1):
        if x1 < 0 or y1 < 0 or x1 > self.Weight or y1 > self.Height:
            return True
        else:
            return False

    def display_die(self, num):
        self.display_score()
        font = pygame.font.SysFont('arial', 80)
        if num % 2 == 1:
            score2 = font.render(f" Try Again With Space ", True, (238, 147, 86))
            self.surface.blit(score2, (120, 420))

        font = pygame.font.SysFont('arial', 300)
        die = font.render("you die", True, (107, 58, 73))
        self.surface.blit(die, (10, 20))
        self.surface.blit(self.surfaceSecond, (0, 0))

    def display_score(self):
        font = pygame.font.SysFont('arial', 18, bold=True)
        score = font.render(f"{self.playerName} : {self.snake.length}", True, (206, 250, 217))
        self.surface.blit(score, (770, 5))

    def display_tutorial(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"  Type your name and Enter !", True, (255, 255, 255))
        self.surface.blit(score, (300, 250))

    def play(self):

        self.surface.blit(self.background_image, (0, 0))
        self.surface.blit(self.surfaceSecond, (0, 0))
        # self.anggryDauTay.move_down()
        self.anggryDauTay.walk()
        self.anggryDauTay.draw()
        for nangluc in self.sieunangluc:
            nangluc.draw()
        self.anotherSnake.draw()
        self.snake.walk()
        self.strawberry.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_ban_muoi(self.snake.x[0], self.snake.y[0]):
            self.running = False

    def gui_va_phan_tach_du_lieu(self):
        dataNhanDuoc = self.network.send(data=[self.snake.color, self.snake.toaDo])
        if dataNhanDuoc is not None:
            ip_tang_diem, dautayXY, toa_do_nguoi_choi_khac = dataNhanDuoc[0], dataNhanDuoc[1], dataNhanDuoc[2]
            self.anotherSnake.set_X_and_Y(toa_do_nguoi_choi_khac)
            self.strawberry.move(dautayXY[0], dautayXY[1])
            if ip_tang_diem is not None:
                if self.tui_la_nguoi_may_man(ip_tang_diem):
                    self.snake.increase_length()
                    self.eatSound.play()

    def getPlayerName(self):
        font = pygame.font.SysFont("arial", 80)
        text_input_box = TextInputBox(210, 300, 600, font)
        group = pygame.sprite.Group(text_input_box)
        run = True
        while run:
            self.clock.tick(60)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        run = False
                if event.type == pygame.QUIT:
                    return "JustQuitPlease"
            group.update(event_list)

            self.surface.fill(0)
            self.display_tutorial()
            group.draw(self.surface)
            pygame.display.flip()
        return text_input_box.text

    def gui_va_dinh_danh(self):
        self.network.mineIP = self.network.getPlayerInfor()
        self.playerName, self.snake.color = self.network.send(self.playerName)

    def run(self):
        hetSlot = False
        print("run")
        self.playerName = self.getPlayerName()
        if self.playerName == "JustQuitPlease":
            return

        print(self.playerName)
        self.zoGameSound.play()
        self.gui_va_dinh_danh()

        while self.running:
            try:
                self.gui_va_phan_tach_du_lieu()
            except pickle.UnpicklingError as fuck:
                print("het slot", fuck)
                hetSlot = True
                break
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
                    if event.key == K_SPACE:
                        self.snake.dash()
                    if event.key == K_q:
                        # switch here
                        self.sieunangluc.append(LaserShot(self.surface, self.snake.x[0], self.snake.y[0], self.snake.direction))
                elif event.type == QUIT:
                    self.running = False

            for nangluc in self.sieunangluc:
                if nangluc.x < self.Weight and nangluc.y < self.Height:
                    nangluc.xulyhuongdan()
                else:
                    self.sieunangluc.pop(self.sieunangluc.index(nangluc))
            self.play()
            print(self.level)
            self.clock.tick(self.level)

        if hetSlot:
            print("out of slot change the port")
            newgame = Game()
            newgame.network.port = self.network.port + 1
            print(newgame.network.port)
            newgame.run()
            return
        else:
            self.network.send(
                self.playerName + "ENDGAME" + str(self.snake.length) + "ENDGAME" + str(self.network.mineIP))
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
                            niugem = Game()
                            niugem.run()
                            return
                    elif event.type == QUIT:
                        return
                self.clock.tick(5)

    def tui_la_nguoi_may_man(self, ip_tang_diem):
        print(ip_tang_diem)
        print(self.network.mineIP)
        self.level += 1
        print(self.level)
        return self.network.mineIP == ip_tang_diem[0]


if __name__ == '__main__':
    game = Game()
    game.run()

#  chơi rắn săn mồi và xếp hình cùng lúc dựa trên cơ chế vừa làm
