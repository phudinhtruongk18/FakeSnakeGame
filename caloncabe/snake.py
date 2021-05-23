import pygame


class Snake:
    def __init__(self, parent_screen,background_image, length):
        self.imageDuoi = pygame.image.load("data/duoi.png").convert()
        self.parent_screen = parent_screen
        self.image = pygame.image.load("data/player.png").convert()
        self.size = self.image.get_size()[0]
        self.direction = 'down'
        self.background_image = background_image

        self.length = length
        self.x = [self.size]*length
        self.y = [self.size]*length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

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
        for i in range(self.length):
            if i == 0:
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.imageDuoi, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
