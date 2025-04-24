import node
import connection
import random

class Brain:
    """ 
    Detta är ett exempel på en hjärna, med attention mekanism. Om andra hjärnor implementeras, bör nätverks-artitekturen ändras.
    Detta uppnås genom att ändra vilka noder som skapas, samt hur de connectar till varandra, i hjärnans init funktion.
    Alltså bör del 1 och del 2 ändras i koden. Samma mall kan användas.
    Om attention-mekanism ej används skall dess tillhörande neuroner raderas, samtidigt som attention funktionen ej anropas.
    """
    def __init__(self, inputs, clone=False):
        # skapar hjärnan med intiala värdern, baserat på om det är en klon
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 4

        if not clone:
            # Skapar perceptroner del 1: 
           
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
                
            #skapar bias i lager 0
            self.nodes.append(node.Node(5))
            self.nodes[5].layer=0

            # skpar 2 neuroner i attention blocket
            for i in [6, 7]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 1
            # skapar bias och output neroen (R^,neuron) i attention-blocket
            self.nodes.append(node.Node(8))
            self.nodes[8].layer = 1
            self.nodes.append(node.Node(9))
            self.nodes[9].layer = 1

           # Skapar 2 neuroner i mellan lager 1 för huvudnätverk
            for i in [10, 11]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 2
            #skapar bias i det riktiga mellanlagret
            self.nodes.append(node.Node(12))
            self.nodes[12].layer = 2

            # Skapar output neuron för hela nätverket
            self.nodes.append(node.Node(13))
            self.nodes[13].layer = 3

            # skapar alla connections, del 2. 
            
            # Skapar connections (linjerna med vikter) till mellanlagret
            for i in [0, 1, 2, 3,4,5]:
                for j in [10,11]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-5, 5)))
            # skapar connections mellan mellan-lagret samt output-neuronen
            for i in [10,11,12]:
                for j in [13]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-5, 5)))
            # skapar connections i attention blocket,
            for i in [6,7,8]:
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[9],
                                                              random.uniform(-5, 5)))
    def connect_nodes(self):
        # Ordnar alla connections, i dem individuella nodernas connections lista
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []
        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])
            
    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def attention(self,node_upp,node_down):
        """Detta är attention blocket,  den har till uppgift att skala input-värden baserad på hur relavnt
        den är just nu. Detta görs genom ett mininäterk
        :parameter dem relevanta noderna, y distans till hålets undre och övre block
        :returns nya ouput värden för dem relevanta noderna"""
        
        for i in [6,7,8,9]:
            self.nodes[i].input_value = 0
            self.nodes[i].output_value = 0
        hole_width=(node_upp.output_value+node_down.output_value)
        number=min(
            [node_upp.output_value,node_upp.output_value])

        if number>0:    y_distance=hole_width/2-number
        elif number<0:  y_distance=hole_width/2+abs(number)
        else:   y_distance=hole_width/2
        if hole_width>0.14: hole_width*=50
        else: hole_width*=-50
            
        self.nodes[6].output_value=hole_width
        self.nodes[7].output_value=y_distance
        self.nodes[8].output_value=1

        for i in [6,7,8,9]:
            self.nodes[i].activate()
        relevance=self.nodes[9].output_value
        node_upp.output_value*=relevance
        node_down.output_value*=relevance

    def feed_forward(self, vision):
        # bestämmer om fåglen vill hoppa eller ej, beoror på inputs och nätverkets artitektur samt vikter
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]
        self.nodes[5].output_value=1
        self.nodes[12].output_value = 1

        # I detta nätverk aktiveras attenion
        for i in [0,2]:
            self.attention(self.nodes[i],self.nodes[i+1])

        #aktiverarr resten av nätverket
        for i in range(0, len(self.net)):
            if i in [6,7,8,9]:
                pass
            self.net[i].activate()

        output_value = self.nodes[13].output_value
        
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0
        return output_value

    def clone(self):
        # klonar en hjärna genom att klona connections och nodes listan; använder sig av understödjande funktioner
        clone = Brain(self.inputs, True)
        for n in self.nodes:
            clone.nodes.append(n.clone())
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))
        clone.layers = self.layers
        clone.generate_net()
       
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    def mutate(self, strength,mutation_type):
        for i in range(0, len(self.connections)):
            self.connections[i].mutate_weight(strength,mutation_type)

