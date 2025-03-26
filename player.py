
import brain
import random
import pygame
import config
import components

class Player:
    def __init__(self):
        # Bird , gameplay
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.death_place=0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()
        self.pipes_passed=[]

    # Game related functions
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
                if pygame.Rect.colliderect(self.rect,pipe_part):
                    value=True
        return value
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision() or self.sky_collision()):
            # Gravity
            self.vel += 0.25
            if self.vel > 5:
                self.vel = 5
            self.rect.y += self.vel

            # Increment lifespan and pipes passed
            self.lifespan += 1
            self.pipe_passing()
        else:
            self.alive = False
            self.flap = False
            self.vel = 0
            self.death_place=self.lifespan
    def pipe_passing(self):
        """ denna funktion kollar om min spelare har passerat en pipe, om så vilken hål
        detta spaars senare vidare i self.pipe_passed"""

        for pipe in config.pipes:
            if pipe.passing:
                hole_ranges=[[sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i - 1]),
                              sum(pipe.pipe_configuration_list[1][0:i]) + sum(pipe.pipe_configuration_list[0][0:i])]
                              for i in range(1,len(pipe.pipe_configuration_list[0])+1)
                             ]


                differance_list=[]
                for hole_group in hole_ranges:
                    differance=hole_group[1]-hole_group[0]
                    differance_list.append(differance)
                differance_list.sort(reverse=True) # störst till minst

                # print(differance_list)
                # print(self.rect.y)

                # med dessa uppgifter kan jag därmed räkna ut vad jag behöver
                for hole_group in hole_ranges:
                    if self.rect.y in range(hole_group[0],hole_group[1]):
                        index=differance_list.index(hole_group[1]-hole_group[0])
                        # print(index)
                        self.pipes_passed.append(index)
        #print("Amount,passed=", len(self.pipes_passed),self.pipes_passed)
    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= -3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p

    # AI related functions
    def look(self):
        pipe=Player.closest_pipe()
        if config.pipes:
            # Line to top pipe
            self.vision[0] = max(0,self.rect.center[1] - pipe.pipe_1.bottom)/500

            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_1.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (pipe.x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0,pipe.pipe_2.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], pipe.pipe_2.top))
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()
    def calculate_fitness(self):
        # fitness ska beror på mängden tid överlevd och hur många hinder jag har sparat och av vilken typ?
        factors=[300,500,700]
        self.fitness = self.lifespan + factors[0]*self.pipes_passed.count(0) + \
                        factors[1]*self.pipes_passed.count(1) + factors[2]*self.pipes_passed.count(2)
        # förklaring: index noll innebär det största hålet, index 1 innebär det näst största hålet och index 2 är det tredje största hålet
        # inse att pipes_passed är en lista som konstant upptaderas  i gamelopopen men resettas vid varje ny population.
    @ staticmethod
    def child(parent_list,parent_group_strength,mutation_type):
        """ denna funktion generarr en ny splerae baserat på föräldrarna genom  att randomly välja mellan deras värden,
        dessutom sker det en viss mutering, basreat på hur bra föräldrarna
       Notera att denna funktion tillgås genom bilkspelarna och resten. Därmed kan type endast vara 1
        """

        offspring=Player()
        # bBrnet har samma nätverksartitektur som föräldrarna, därmed behöver vi endast ändra vikterna
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
