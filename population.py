import random
import config
import player
import math
import operator
import copy
import statistics

class Population:
    def __init__(self, size):
        #initierar alla värden
        self.players = []
        self.generation = 1
        self.size = size
        for i in range(0, self.size):
            self.players.append(player.Player())
        self.species = []

        # nautural selection relatede konstanter:
        self.group_size=4 
        self.parent_size=3 
        self.weak_survival_chance=0.05
        self.weak_parent_chance=0.05
        self.best_players_copies=10
        self.new_genetic_players=5

        # Mutations relaterade parametrar
        self.target_fitness=12000
        self.mutation_types=[0,1,2]  


        # Graf relaterade värden
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

    def calculate_population_fitness(self):
        #kalkylerar fittnes
        for p in self.players:
            p.calculate_fitness()
    def population_grouping(self):
        #grupperar populationen
        player_list=copy.deepcopy(self.players)
        random.shuffle(player_list)
        group_amount=int(len(player_list)/self.group_size)
        population_groups=[player_list[i:i+self.group_size]
                           for i in range(0,len(player_list),self.group_size)
                           ]
        if len(population_groups[-1])==1:
            removed_item= population_groups.pop(-1)
            population_groups[-1].append(removed_item[0])
        return population_groups
    def selection(self,population_group_list):
        #sållar bort indivderna utefrån selektions-metoden
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
        current_selected_group_list= [individual for group in selected_group_list for individual in group] #Tar bort inomboendes struktur
        random.shuffle(current_selected_group_list)

        # Väler ut föräldrar grupper utefrån en probobalistisk metod
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
            parent_list.append(parent_list_sub_part)
            
        # Bestämmer styrkan på varje föäldrar grupp- och därav hur mycket dess barn bör muteras.
        relative_group_strength = []
        for group in parent_list:
            values=[p.fitness for p in group]
            median_strength=statistics.median(values)
            relative_group_strength.append(median_strength)

        children_amount=int(
            (len(self.players)-self.new_genetic_players-self.best_players_copies)
            /len(parent_list)
        )

        #nedanför följer själva skapndet av den nya generationer
        for i in range(0,len(parent_list)):
            for _ in range(0,children_amount):
                child=player.Player.child(parent_list[i],relative_group_strength[i],self.mutation_types[0])
                next_generation.append(child)
        
        for i in range(self.new_genetic_players):
            person=random.choice(random.choice(parent_list)).clone()
            person.brain.mutate(self.fitness_list[-1][1],self.mutation_types[1])
            person.brain.generate_net()
            next_generation.append(person)
       
        current_selected_group_list.sort(key=operator.attrgetter('fitness'),reverse=True)
        for i in range(self.best_players_copies):
            child=current_selected_group_list[i].clone()
            next_generation.append(child)
       
        while len(next_generation)<len(self.players):
            chosen_group=random.choice(parent_list)
            child=player.Player.child(chosen_group, relative_group_strength[parent_list.index(chosen_group)],self.mutation_types[0])
            next_generation.append(child)
      
        
        random.shuffle(next_generation)
        self.players=[]
        for p in next_generation:
            self.players.append(p)
    

    def visualize(self):
        """  Inhämtar informationen som skall användas i visualiseringen; fittnes, dödsplats, genetisk standart-avikelse 
        """

        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        
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


    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
