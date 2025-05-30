import random
import math

class Connection:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    @staticmethod
    def mutation_distribution(factor,strength): # Muterar efter täthets förderlning.
        sigma = 2080
        mean = 0
        original_factor = 3750

        value= factor* original_factor * (
                1/(sigma*math.sqrt(math.pi*2)) *
                math.exp((-1/2)*((strength-mean)/sigma)**2))
        return value

    def mutate_weight(self,strength,mutation_type):
        mutation_factors = [1,1.7,2.4]
        mutation_probabilities = [0.20, 0.40, 1]
        value=random.uniform(0,1)

        if value<=mutation_probabilities[mutation_type]:  # Vill mutera
            mutation_step=Connection.mutation_distribution(mutation_factors[mutation_type],strength)
            self.weight=random.uniform(self.weight-mutation_step,self.weight+mutation_step)

        # kollar mina gränser.
        if self.weight > 5:
            self.weight = 5
        if self.weight <- 5:
            self.weight =- 5

    def clone(self, from_node, to_node):
        clone = Connection(from_node, to_node, self.weight)
        return clone
