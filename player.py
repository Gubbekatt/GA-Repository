import brain
import random
import pygame
import config

class Player:
    def __init__(self):
        # Spel-mekanik
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.death_place=0

        # Ai
        self.decision = None
        self.vision = [0.5, 1, 0.5,1,0.5]
        self.fitness = 0
        self.inputs = 5
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()
        self.pipes_passed=[]

    # Funktioner för spelmekanik
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision() or self.sky_collision()): # ingen kollision
            # Gravity
            self.vel += 0.25
            if self.vel > 5:
                self.vel = 5
            self.rect.y += self.vel

            # Uppdaterar spelarens livs-situation; Hur länge lever den och antal hål passerade
            self.lifespan += 1
            self.pipe_passing()
        else: # Spelaren är vid denna frame och alla frammåt ej vid liv.
            self.alive = False
            self.flap = False
            self.vel = 0
            self.death_place=self.lifespan
    def bird_flap(self):
        if not self.flap and not self.sky_collision(): # Fågelns vill och får hoppa. Bestäms i Think.
            self.flap = True
            self.vel = -5
        if self.vel >= -3:
            self.flap = False

    # Funktioner för kollisioner med marken, himmeln och närmsta pipsen.
    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    def sky_collision(self):
        return bool(self.rect.y < 30)
    def pipe_collision(self):
        value=False
        for pipe in config.pipes:
            for pipe_part in pipe.pipe_list:
                if pygame.Rect.colliderect(self.rect,pipe_part):
                    value=True
        return value

    # AI relaterade funktioner
    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p
    def look(self):
        pipe=Player.closest_pipe()
        if config.pipes: # fyller spelarens vision för vare frame.
            # Två håls layout
            # Line to top pipe
            self.vision[0] = (self.rect.center[1] - pipe.pipe_1.bottom)/500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_1.bottom))

            # Line to bottom pipe
            self.vision[1] = (pipe.pipe_2.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_2.top))

            # Line to mid pipe
            self.vision[4] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (pipe.x, self.rect.center[1]))

            # line to top in hole 2
            self.vision[2] = (self.rect.center[1] - pipe.pipe_2.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_1.bottom))


            # Line to bottom in hole 2
            self.vision[3] = (pipe.pipe_3.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_2.top))
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73: # Vill hoppa, men får jsg hoppa?
            self.bird_flap()


    # Naturlig selektion funktioner
    def pipe_passing(self):
        for pipe in config.pipes:
            if pipe.passing: # Just nu passeras ett hål. Spara vilken sort den är i self.pipe_passed
                hole_ranges=[[sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i - 1]),
                              sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i])]
                             for i in range(1,len(pipe.pipe_configuration_list[0])+1)
                             ]
                differance_list=[]
                for hole_group in hole_ranges:
                    differance=hole_group[1]-hole_group[0]
                    differance_list.append(differance)
                differance_list.sort(reverse=True)

                for hole_group in hole_ranges:
                    if self.rect.y in range(hole_group[0],hole_group[1]):
                        index=differance_list.index(hole_group[1]-hole_group[0])
                        self.pipes_passed.append(index)
    def calculate_fitness(self): #Dags för naturlig selektion. ´Vilken fittnes har individen?
        factors = [300, 500, 700]
        self.fitness = self.lifespan + factors[0] * self.pipes_passed.count(0) + \
                       factors[1] * self.pipes_passed.count(1) + factors[2] * self.pipes_passed.count(2)
    @staticmethod
    def child(parent_list, parent_group_strength, mutation_type):

        offspring = Player() # Skapar tomt-barn

        for i in range(0, len(offspring.brain.connections)): # Väljs vikter och potentiellt mutera.
            weight_choices = [
                parent.brain.connections[i].weight
                for parent in parent_list
            ]
            offspring.brain.connections[i].weight = random.choice(weight_choices)

            offspring.brain.connections[i].mutate_weight(parent_group_strength, mutation_type)

        offspring.brain.generate_net() # Färdig ställ hjärnan

        return offspring
    def clone(self):
        clone = Player()
        clone.fitness = 0
        clone.brain = self.brain.clone() # Klona hjärnan men håll spelaren tom i allmänhet.
        return clone
