import brain
import random
import pygame
import config

class Player:
    def __init__(self):
        # Game-play related function. Initial condition
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.death_place=0

        # AI related parametars, intitiala värden. 
        self.decision = None
        self.vision = [0.5, 1, 0.5 , 0.5 ,0.5]
        self.fitness = 0
        self.inputs = 5
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()
        self.pipes_passed=[]

    # Nedanför följer alla spel relaterade funktioner. 
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    def sky_collision(self):
        return bool(self.rect.y < 30)
    def pipe_collision(self):
        value=False
        for pipe in config.pipes:
            for pipe_part in pipe.pipe_list:
                if pygame.Rect.colliderect(self.rect,pipe_part):    value=True
        return value
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision() or self.sky_collision()):
            # ändrar spelarens hastighet och y posetion utefrån en gravitations modell. 
            self.vel += 0.25
            if self.vel > 5:
                self.vel = 5
            self.rect.y += self.vel

            # ökar life span, samt håller räkning på antal hål passerade.
            self.lifespan += 1
            self.pipe_passing()
        else:
            self.alive = False
            self.flap = False
            self.vel = 0
            self.death_place=self.lifespan
    def pipe_passing(self):
        """Denna funktion obsarverar antal hål passerade, samt vilken sorts hål det är 
        """

        for pipe in config.pipes:
            if pipe.passing:
                # Hittar alla hålen av den relevanta pipen, samt deras respektive distanser
                hole_ranges=[[sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i - 1]),
                              sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i])]
                              for i in range(1,len(pipe.pipe_configuration_list[0])+1)
                             ]
                differance_list=[]
                for hole_group in hole_ranges:
                    differance=hole_group[1]-hole_group[0]
                    differance_list.append(differance)
                differance_list.sort(reverse=True)

                # FInner vilket sorts hål, den passerar och sparar den informationen.
                for hole_group in hole_ranges:
                    if self.rect.y in range(hole_group[0],hole_group[1]):
                        index=differance_list.index(hole_group[1]-hole_group[0])
                        self.pipes_passed.append(index)
    def bird_flap(self):
        # tillåter fågeln hoppa genom att ändra dess hastighet direkt.
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= -3:
            self.flap = False
    @staticmethod
    def closest_pipe():
        # hittar den närmsta pipen i relation till spelaren
        for p in config.pipes:
            if not p.passed:
                return p

    # Vidare följer samtliga Ai reletarde funktioner, vilket inefattar vision samt förmågan att ta beslut;
    def look(self):
        pipe=Player.closest_pipe()
        if config.pipes:
            # distans till top-delen i hål 1
            self.vision[0] = (self.rect.center[1] - pipe.pipe_1.bottom)/500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_1.bottom))

            # Distans till bottom del i hål 1
            self.vision[1] = (pipe.pipe_2.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_2.top))

            # Distans till top del i hål 2
            self.vision[2] = ( self.rect.center[1] - pipe.pipe_2.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_2.bottom))

            # Distans till bottom del i hål 2
            self.vision[3] = ( pipe.pipe_3.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_3.top))

            # x distans till själva pipen
            self.vision[4] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (pipe.x, self.rect.center[1]))
    def think(self):
        self.decision = self.brain.feed_forward(self.vision) # Hur mycket vill den hoppa
        if self.decision > 0.73:
            self.bird_flap()
    def calculate_fitness(self):
        factors=[300,500,700]
        self.fitness = self.lifespan + factors[0]*self.pipes_passed.count(0) + \
                        factors[1]*self.pipes_passed.count(1) + factors[2]*self.pipes_passed.count(2)
    @ staticmethod
    def child(parent_list,parent_group_strength,mutation_type):
        """ denna funktion generarr en ny splerae baserat på föräldrarna genom  att randomly välja mellan deras värden,
        Dessutom sker det en viss mutering, baserat på hur bra föräldrarna är
        """
        offspring=Player()
        for i in range(0,len(offspring.brain.connections)):
            weight_choices=[
                parent.brain.connections[i].weight
                for parent in parent_list
            ]
            offspring.brain.connections[i].weight=random.choice(weight_choices)
            offspring.brain.connections[i].mutate_weight(parent_group_strength,mutation_type)
        offspring.brain.generate_net()
        return offspring
    def clone(self):
        clone = Player()
        clone.fitness = 0
        clone.brain = self.brain.clone()
        return clone
