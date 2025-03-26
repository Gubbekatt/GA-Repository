import random
from numpy.ma.extras import average
import config
import player
import math
import species
import operator
import copy
import math
import statistics


""" ok här i polutaions delen av koden vill jag inte ändra hur den hanterar spelare utan bara ändra i speciet funktionen """

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.size = size
        for i in range(0, self.size):
            self.players.append(player.Player())
        self.species = []

        # nautural selection related constant:
        self.group_size=4  # i hum stoa grupper ska vi dela i selektionen?
        self.parent_size=3 # hur många förldrar ska varje barn ha
        self.weak_survival_chance=0.05
        self.weak_parent_chance=0.05
        self.best_players_copies=10
        self.new_genetic_players=5

        # dynamic mutauin related constants
        self.target_fitness=12000
        self.mutation_types=[0,1,2]  # 0 innebär en vanlig player mutation, 1 är nya gentiska spelare och 2 är en krismutation


        # graph related attributes
        self.fitness_list=[]
        self.median_fitness=0
        self.top_procent_fitness=0
        self.bottom_procent_fitness=0
        self.procent_selection=0.1
        self.death_place_list=[]
        self.weight_st_variation_list=[]

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                # print("index=",self.players.index(p))
                p.look()
                p.think()
                p.draw(config.window)
                p.update(config.ground)
    def natural_selection(self):
        self.calculate_population_fitness()
        self.visualize()
        group_list=self.population_grouping()
        group_list_selected=self.selection(group_list)
        self.next_generation(group_list_selected)
        #self.crisis_mutation()

    def calculate_population_fitness(self):
        # räknar ut spelare fitness enligt funktionen som finns i player klassen
        for p in self.players:
            p.calculate_fitness()
    def population_grouping(self):
        player_list=copy.deepcopy(self.players)
        random.shuffle(player_list)
        # print([p.fitness for p in player_list])
        # print("lengt of players =", len(player_list))
        group_amount=int(len(player_list)/self.group_size) # hur många i varje grupp
        population_groups=[player_list[i:i+self.group_size]
                           for i in range(0,len(player_list),self.group_size)
                           ]
        if len(population_groups[-1])==1:
            removed_item= population_groups.pop(-1)
            population_groups[-1].append(removed_item[0])
        # print(population_groups)
        # print(len(population_groups),len(population_groups[0]))
        return population_groups
    def selection(self,population_group_list):
        for group in population_group_list:
            value=random.uniform(0,1)
            group.sort(key=operator.attrgetter('fitness'),reverse=True)
            if value<self.weak_survival_chance:
                chosen_player=random.sample(group[1:],1)
                group[:]=chosen_player
            else:
                group[:]=[group[0]]


        return population_group_list
    def next_generation(self,selected_group_list):
        next_generation=[]

        current_selected_group_list= [individual for group in selected_group_list for individual in group] # tar bort inre struktur
        random.shuffle(current_selected_group_list)
        # print(current_selected_group_list,  [p.fitness  for p in current_selected_group_list])
        # print(len(current_selected_group_list) )

        parent_group_amount=int(
            len(current_selected_group_list)/self.parent_size
        )

        parent_list=[]
        for i in range(0, parent_group_amount):
            parent_list_sub_part = []
            for j in range(0,self.parent_size):
                possible_parents=random.sample(current_selected_group_list,5)
                possible_parents.sort(key=operator.attrgetter('fitness'),reverse=True)
                value=random.uniform(0,1)
                if value<self.weak_parent_chance:
                    chosen_parent=random.choice(possible_parents[1:])
                else:
                    chosen_parent=possible_parents[0]
                parent_list_sub_part.append(chosen_parent)
            parent_list.append(parent_list_sub_part)  # alla grupper nu lika stora, fylle rinte upp listan helt.
        # print("parent:list time!", parent_list)
        # print([j.fitness for item in parent_list for j in item])
        # print(len([item for item in parent_list]))
        # print(len( [j.fitness for item in parent_list for j in item]))

        relative_group_strength = []
        for group in parent_list:
            values=[p.fitness for p in group]
            median_strength=statistics.median(values)
            relative_group_strength.append(median_strength)
        # print("how strong is each group?", relative_group_strength)

        children_amount=int(
            (len(self.players)-self.new_genetic_players-self.best_players_copies)
            /len(parent_list)
        )
       # print(children_amount)
        for i in range(0,len(parent_list)):
            for _ in range(0,children_amount):
                child=player.Player.child(parent_list[i],relative_group_strength[i],self.mutation_types[0])
                next_generation.append(child)
        # print("bulk of polayers",len(next_generation))
        for i in range(self.new_genetic_players):
            person=random.choice(random.choice(parent_list)).clone()
            person.brain.mutate(self.fitness_list[-1][1],self.mutation_types[1])
            person.brain.generate_net()
            next_generation.append(person)
        # print("ok new ones", len(next_generation))
        current_selected_group_list.sort(key=operator.attrgetter('fitness'),reverse=True)
        for i in range(self.best_players_copies):
            child=current_selected_group_list[i].clone()
            next_generation.append(child)
        # print("with the copies", len(next_generation))
        while len(next_generation)<len(self.players):
            chosen_group=random.choice(parent_list)
            child=player.Player.child(chosen_group, relative_group_strength[parent_list.index(chosen_group)],self.mutation_types[0])
            next_generation.append(child)
        # print("evry one", len(next_generation))

        random.shuffle(next_generation)
        self.players=[]
        for p in next_generation:
            self.players.append(p)
    def crisis_mutation(self):
        """ denna funktion har till uppgift att påbörja en genomgående muteirng om
        evolutionesn har stagnerat"""

        if self.generation%75==0 and self.generation>=75:  # gör det var 75 generation
            fitness_derivative= ( self.fitness_list[self.generation-2][1]-self.fitness_list[self.generation-2-75][1])\
                               /75
            print(fitness_derivative)
            if fitness_derivative<=12:
                for p in self.players:
                    p.brain.mutate(self.fitness_list[-1][1],self.mutation_types[2])
                print("happend")

    def visualize(self):
        """ denna funktion har till uppgift att genrerera den datan som behövs
            ska göra median grafer,och döds kurvan. tillsut även den entiska diskbutionen            """

        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        # använder ovan data för att räkna ut framågng öf rarten
        self.median_fitness = self.players[int(len(self.players) / 2)].fitness
        self.top_procent_fitness = self.players[int(
            int(self.procent_selection * len(self.players)) / 2
        )].fitness
        self.bottom_procent_fitness = self.players[-int(
            int(self.procent_selection * len(self.players)) / 2
        )].fitness
        self.fitness_list.append([self.bottom_procent_fitness,self.median_fitness,self.top_procent_fitness])

        self.death_place_list=[p.death_place for p in self.players]

        weight_mean_value_list =[]
        for i in range(0,len(self.players[0].brain.connections)):
            weight_mean_value=sum([p.brain.connections[i].weight for p in self.players])/len(self.players)
            weight_mean_value_list.append(weight_mean_value)
        instence_list=[]
        for i in range(0,len(self.players[0].brain.connections)):
            a=[p.brain.connections[i].weight for p in self.players]
            weight_st_variation_value=math.sqrt(
                                       sum(
                                           [(relevant_weight-weight_mean_value_list[i])**2 for relevant_weight in a]
                                       )*(1/len(self.players))
                                        )
            instence_list.append(weight_st_variation_value)
        self.weight_st_variation_list.append(instence_list)

        self.generation += 1





    # Return true if all players are dead
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
