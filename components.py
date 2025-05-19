import pygame
import random
import exprimentation

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 20)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:

    width = 16
    opening = 100
    holes=2
    pipe_list=exprimentation.a

    def __init__(self, win_width):
        # Pipes egenskaper
        self.x = win_width
        self.pipe_configuration_list = random.choice(Pipes.pipe_list)
        self.pipe_1, self.pipe_2 = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.pipe_3, self.pipe_4 = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.pipe_list=[]

        # Game related functions
        self.passed = False
        self.passing = False
        self.off_screen = False

    def draw(self, window):
        # Programmet ritar pipes baseradde på hur många det finns.

        self.pipe_1 = pygame.Rect(self.x, 0, self.width, self.pipe_configuration_list[1][0])
        self.pipe_2 = pygame.Rect(self.x, self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0],
                                  self.width,
                                  self.pipe_configuration_list[1][1])

        if len(self.pipe_configuration_list[1]) >= 3: # två hål
            self.pipe_3 = pygame.Rect(self.x,
                                  self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0] +
                                  self.pipe_configuration_list[1][
                                      1] + self.pipe_configuration_list[0][1],
                                  self.width, +self.pipe_configuration_list[1][2])

        if len(self.pipe_configuration_list[1]) >= 4: # tre hål
            self.pipe_4 = pygame.Rect(self.x,
                                      self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0] +
                                      self.pipe_configuration_list[1][
                                          1] + self.pipe_configuration_list[0][1] + self.pipe_configuration_list[1][2] +
                                      self.pipe_configuration_list[0][2],
                                      self.width, +self.pipe_configuration_list[1][3])

        if Pipes.holes == 1:
            self.pipe_list[:] = [self.pipe_1,self.pipe_2]
        if Pipes.holes == 2:
            self.pipe_list[:] = [self.pipe_1, self.pipe_2,self.pipe_3]
        if Pipes.holes == 3:
            self.pipe_list[:] = [self.pipe_1, self.pipe_2,self.pipe_3,self.pipe_4]

        pygame.draw.rect(window, "White", self.pipe_1)
        pygame.draw.rect(window, "White", self.pipe_2)
        pygame.draw.rect(window, "White", self.pipe_3)
        pygame.draw.rect(window, "White", self.pipe_4)

    def update(self):
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True

        if self.x <= -self.width: # Utan för skärmen
            self.off_screen = True

        bird_dimensions=[60,20]
        if self.x+Pipes.width/2 ==60: # har passeratt en fågel ?
            self.passing=True
        else:
            self.passing=False
