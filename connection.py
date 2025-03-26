
import random
import math


"""ändra inget förutom mutations funktoinen för den, """

class Connection:
    def __init__(self, from_node, to_node, weight):

        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    @staticmethod
    def mutation_distribution(factor,strength):
        #print("Values comming in are,", str(factor),str(strength))
        sigma=2080
        mean=0
        original_factor=3750
        value= factor* original_factor * (
                1/(sigma*math.sqrt(math.pi*2)) *
                math.exp((-1/2)*((strength-mean)/sigma)**2)
                )
        # print("mutation is", value)
        # print()
        return value





    def mutate_weight(self,strength,mutation_type):
        """ denna funktion muterar en vikt inom en range baserat på styrkan och hur vilken typr det är
        notera: 0 = vabliga nya spleare, 1=gentiska spelare   2= cris mutation"""

        # orndingen på indexen är den samma som ovan
        mutation_factors=[1,1.5,2.4]
        mutation_probabilities=[0.15 , 0.3, 1]

        value=random.uniform(0,1)
        if value<=mutation_probabilities[mutation_type]:
            mutation_step=Connection.mutation_distribution(mutation_factors[mutation_type],strength)
            self.weight=random.uniform(self.weight-mutation_step,self.weight+mutation_step)
        if self.weight>5:
            self.weight=5
        if self.weight<-5:
            self.weight=-5
    def clone(self, from_node, to_node):
        clone = Connection(from_node, to_node, self.weight)
        return clone
