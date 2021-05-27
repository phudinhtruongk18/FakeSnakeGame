import pickle
import socket
import pygame
from pygame.locals import *
from textInput import TextInputBox


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


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.2.58"
        self.port = 65432
        # self.client.get
        self.mineIP = ""
        self.addr = ()
        self.p = ""

    def getPlayerInfor(self):
        print("toi ne ", self.port)
        self.addr = (self.server, self.port)
        self.p = self.connect()
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except socket.error as e:
            print("Hok the ket noi ", e)

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
        self.clock = pygame.time.Clock()
        self.Height = 694
        self.Weight = 1015
        self.running = True
        self.surface = pygame.display.set_mode((self.Weight, self.Height))
        self.surfaceSecond = pygame.display.set_mode((self.Weight, self.Height))
        self.background_image = pygame.image.load("tainguyen/seaBG.png").convert()
        self.surface.blit(self.background_image, (0, 0))
        self.surface.blit(self.surfaceSecond, (0, 0))
        # self.surfaceSecond.blit(self.background_image,(0,0))
        self.snake = Snake(self.surface, self.surfaceSecond, 2, "#5404CA")
        self.snake.draw()
        self.anotherSnake = AnotherSnake(parent_screen=self.surface, parent_screen_image=self.surfaceSecond,
                                         x=20, y=20)
        self.anotherSnake.draw()
        self.strawberry = Strawberry(self.surface)
        self.strawberry.draw()
        if self.strawberry.size == self.snake.size:
            self.size = self.strawberry.size
        else:
            return
        self.level = 3
        self.playerName = "No Name"
        self.eatSound = pygame.mixer.Sound("tainguyen/eat.wav")
        self.zoGameSound = pygame.mixer.Sound("tainguyen/heheboiz.wav")

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
        self.level += 2
        print(self.level)
        return self.network.mineIP == ip_tang_diem[0]


if __name__ == '__main__':
    game = Game()
    game.run()
