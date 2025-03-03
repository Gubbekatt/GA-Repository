import brain
import random
import pygame
import config



class Player:
    def __init__(self):
        # Bird

        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5,1,0.5,0.5,0.5]
        self.fitness = 0
        self.inputs = 7
        self.brain = brain.Brain(self.inputs) # behöver veta vilka inp0uts vi tar från pipes 
        self.brain.generate_net()

    # Game related functions
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.pipe_1) or \
                   pygame.Rect.colliderect(self.rect, p.pipe_2) or pygame.Rect.colliderect(self.rect, p.pipe_3) or pygame.Rect.colliderect(self.rect, p.pipe_4)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            # Increment lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= -5:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes: # det finns inget av pipe_1 och pipe-2
            if not p.passed:
                return p

    # AI related functions
    def look(self):

        item = Player.closest_pipe() # varför får jag error message i population när jag byter från Player.closest_pipe()


        if config.pipes:

            # Line to top pipe
            self.vision[0] = (max(0, self.rect.center[1] - item.pipe_1.bottom) / 500)
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_1.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, item.x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, item.pipe_2.top  - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_2.top))
            # en öppning klar

            # övre andra öppning
            self.vision[3] = (max(0, self.rect.center[1] - item.pipe_2.bottom) / 500)
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_2.bottom))

            # lägre andra öppning
            self.vision[4] = max(0, item.pipe_3.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_3.top))
            # övre tredje öppning
            self.vision[5] = (max(0, self.rect.center[1] - item.pipe_3.bottom) / 500)
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_3.bottom))


            # lägre tredje öppning
            self.vision[6] = max(0, item.pipe_4.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].pipe_4.top))


    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone