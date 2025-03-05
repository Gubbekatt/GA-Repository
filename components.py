import pygame
import random
def generate_hole_and_pipe_lengths(total_span):
    """ Denna funktion har till uppgift att generera, en lista på hur lång respketive
     öppning och pipe ska vara, samt i vilken ordning allting kommer. Allt efter kraven"""
    pipe_length_list=[]
    hole_length_list=[]
    pipe_min_length=40
    hole_min_length=65
    minimum_hole_diff=5
    minimum_hole_list=[hole_min_length+2*minimum_hole_diff,hole_min_length+minimum_hole_diff,hole_min_length]
    hole_max_length=100

    # Först: hur mycket extra får varje block och hål, utöver minimum kraven?
    extra_hole_pixels=[0,0,0]
    hole_length_differance=[0,0]
    while any(number<minimum_hole_diff for number in hole_length_differance):
        hole_length_list.clear()
        for i in range(0, len(extra_hole_pixels)):
            extra_hole_pixels[i]=random.randrange(0,hole_max_length-minimum_hole_list[i])
        for i in range(0,len(extra_hole_pixels)):
            hole_length_list.append(extra_hole_pixels[i]+ minimum_hole_list[i] )
        hole_length_list.sort(reverse=True)
        for i in range(0,2):
            hole_length_differance[i]=hole_length_list[i]-hole_length_list[i+1]


    # Baserat på hur mycket jag har kvar att alokela. Hur mycket ska varje block få, utöver minimun längd?
    pipe_length_allocate=total_span-sum(hole_length_list)-4*pipe_min_length
    cuts = sorted(random.sample(range(0, pipe_length_allocate), 3))
    cuts.sort(reverse=False)

    pipe_length_list.append(cuts[0]+pipe_min_length)
    pipe_length_list.append(cuts[1]-cuts[0]+pipe_min_length)
    pipe_length_list.append(cuts[2]-cuts[1]+pipe_min_length)
    pipe_length_list.append(pipe_length_allocate-cuts[2]+pipe_min_length)

    # nu slumpar vi ordningen på alla värden
    random.shuffle(pipe_length_list)
    random.shuffle(hole_length_list)

    return hole_length_list,pipe_length_list

#x,y=generate_hole_and_pipe_lengths(700)
n=0
lista=[]
while n<1000:
    a,b=generate_hole_and_pipe_lengths(500)
    if [a,b] not in lista:
        lista.append(  [a,b] )
    n+=1

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 15

    def __init__(self, win_width):
        self.pipe_configuration_list = random.choice(lista)
        self.x = win_width
        self.passed = False
        self.off_screen = False
        self.pipe_1, self.pipe_2,self.pipe_3,self.pipe_4 = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0),pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)

    def draw (self,window):

        self.pipe_1 = pygame.Rect(self.x, 0, self.width, self.pipe_configuration_list[1][0])
        self.pipe_2 = pygame.Rect(self.x, self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0], self.width,
                                  self.pipe_configuration_list[1][1])
        self.pipe_3 = pygame.Rect(self.x,
                                  self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0] +
                                  self.pipe_configuration_list[1][
                                      1] + self.pipe_configuration_list[0][1],
                                  self.width, +self.pipe_configuration_list[1][2])
        self.pipe_4 = pygame.Rect(self.x,
                                  self.pipe_configuration_list[1][0] + self.pipe_configuration_list[0][0] +
                                  self.pipe_configuration_list[1][
                                      1] + self.pipe_configuration_list[0][1] + self.pipe_configuration_list[1][2] +
                                  self.pipe_configuration_list[0][2],
                                  self.width, +self.pipe_configuration_list[1][3])

        pygame.draw.rect(window, "White", self.pipe_1)
        pygame.draw.rect(window, "White", self.pipe_2)
        pygame.draw.rect(window, "White", self.pipe_3)
        pygame.draw.rect(window, "White", self.pipe_4)

    def update(self):
        self.x -= 1.5
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True
            
class Hinder:
    def __init__(self, win_height):
        self.length = random.randint(50, 100)
        self.x = 700
        self.y = 500 - self.length
        self.width = 15
        self.vel_y = random.uniform(1, 1.5)
        self.vel_x = 1.5
        self.rect = pygame.Rect(0,0,0,0,)
        self.offscreen_y = False
        self.offscreen_x = False
        self.passed = False
        self.direction = 1

    def draw(self,window):
        self.rect =  pygame.Rect(self.x,self.y,self.width,self.length)
        pygame.draw.rect(window, (255,255,255), self.rect)

    def update(self):
        self.y -= self.vel_y * self.direction
        self.x -= self.vel_x
        if self.y <= 0 or self.y >= 500 - self.length:
            self.offscreen_y = True
        else:
            self.offscreen_y = False
        if self.x <= 0:
            self.offscreen_x = True
        else:
            self.offscreen_x = False
        if self.x + self.width <= 50:
            self.passed = True