import random
import sys
import pygame



def load_image(name, colorkey=None):
    image = pygame.image.load(name).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        elif colorkey == -2:
            colorkey = image.get_at((1, 35))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 750))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.message = load_image("data/message.png", -1)
        self.background = pygame.image.load("data/backtest.png").convert()
        self.base = pygame.image.load("data/base1.png").convert()

        self.birdSprites = [load_image("data/blackbird_1.png", -1),
                            load_image("data/blackbird_0.png", -1),
                            load_image("data/blackbird_2.png", -1),
                            load_image("data/dead.png", -1)]
        for i in range(len(self.birdSprites)):
            self.birdSprites[i] = pygame.transform.scale(self.birdSprites[i], (41, 28))

        self.wallUp = load_image("data/bottom_test.png", -1)
        self.wallDown = load_image("data/top_test.png", -1)

        self.NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.NUMBERS = list(map(lambda x: pygame.transform.scale(
            load_image('data/{}.png'.format(x), -2), (30, 45)), self.NUMBERS))

        self.gap = 140
        self.basex = 0
        self.wallx_1 = 400
        self.wallx_2 = 650
        self.birdY = 350
        self.jump = 10
        self.jumpSpeed = 10
        self.gravity = 3
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset_1 = random.randint(-110, 110)
        self.offset_2 = random.randint(-110, 110)

    def updateBase(self):
        self.basex -= 3
        if self.basex <= -192:
            self.basex = 0

    def updateWalls(self):
        self.wallx_1 -= 3
        self.wallx_2 -= 3
        if self.wallx_1 < -100:
            self.wallx_1 = 400
            self.offset_1 = random.randint(-110, 110)
        if self.wallx_2 < -100:
            self.wallx_2 = 400
            self.offset_2 = random.randint(-110, 110)
        if 0 <= self.wallx_1 <= 2:
            self.counter += 1
        if 0 <= self.wallx_2 <= 2:
            self.counter += 1

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.3
        self.bird[1] = self.birdY

        upRect_1 = pygame.Rect(self.wallx_1,
                             360 + self.gap - self.offset_1 + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect_1 = pygame.Rect(self.wallx_1,
                               0 - self.gap - self.offset_1 - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())

        upRect_2 = pygame.Rect(self.wallx_2,
                               360 + self.gap - self.offset_2 + 10,
                               self.wallUp.get_width() - 10,
                               self.wallUp.get_height())
        downRect_2 = pygame.Rect(self.wallx_2,
                                 0 - self.gap - self.offset_2 - 10,
                                 self.wallDown.get_width() - 10,
                                 self.wallDown.get_height())

        # if upRect_1.colliderect(self.bird) or upRect_2.colliderect(self.bird):
        #     self.dead = True
        # if downRect_1.colliderect(self.bird) or downRect_2.colliderect(self.bird):
        #     self.dead = True
        if self.birdY >= 600:
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 350
            self.birdY = 350
            self.dead = False
            self.counter = 0
            self.basex = 0
            self.wallx_1 = 400
            self.wallx_2 = 650
            self.offset_1 = random.randint(-110, 110)
            self.gravity = 2

    def start(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        self.bird[1] = 350
        self.birdY = 350
        self.dead = False
        self.counter = 0
        self.basex = 0
        self.wallx_1 = 400
        self.wallx_2 = 650
        self.offset_1 = random.randint(-110, 110)
        self.jump = 10
        self.gravity = 2
        self.jumpSpeed = 10
        frames_per_second = 0
        while True:
            clock.tick(60)
            frames_per_second += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.run()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.base, (self.basex, 650))
            self.screen.blit(self.message, (108, 150))

            if frames_per_second // 5 == 1:
                self.sprite = 0
            elif frames_per_second // 5 == 2:
                self.sprite = 1
            elif frames_per_second // 5 == 3:
                self.sprite = 2
                frames_per_second = 0
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))

            self.updateBase()
            pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 10
                    self.gravity = 2
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            self.screen.blit(self.wallUp,
                             (self.wallx_1, 360 + self.gap - self.offset_1))
            self.screen.blit(self.wallDown,
                             (self.wallx_1, 0 - self.gap - self.offset_1))

            self.screen.blit(self.wallUp,
                             (self.wallx_2, 360 + self.gap - self.offset_2))
            self.screen.blit(self.wallDown,
                             (self.wallx_2, 0 - self.gap - self.offset_2))

            self.screen.blit(self.base, (self.basex, 650))

            self.totalX = (400 - len(str(self.counter))) // 2
            for i in range(len(str(self.counter))):
                self.screen.blit(self.NUMBERS[int(str(self.counter)[i])], (self.totalX + 24 * i, 70))

            if self.dead:
                self.sprite = 3
                self.birdY -= 10
            elif self.jump:
                self.sprite = 2
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateBase()
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()
            if self.dead:
                self.start()


if __name__ == "__main__":
    FlappyBird().start()