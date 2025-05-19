import node
import connection
import random

class Brain:
    """
    Denna hjärna är en all to two with bias och linjär attention. Samma dynamik
    fungerar dock på andra hjärnor.
    """
    # Skapa hjärnarttekturen
    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 4

        if not clone:
            # Skapar perceptroner
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

            # skapar bias och output neuronen (R^,neuron)
            self.nodes.append(node.Node(8))
            self.nodes[8].layer = 1
            self.nodes.append(node.Node(9))
            self.nodes[9].layer = 1

           # Skapar 2 neuroner i riktiga mellan lagret
            for i in [10, 11]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 2

            #skapar bias i det riktiga mellanlagret
            self.nodes.append(node.Node(12))
            self.nodes[12].layer = 2

            # Skapar output neuron för hela nätverket
            self.nodes.append(node.Node(13))
            self.nodes[13].layer = 3

            # Skapar connections (linjerna med vikter) till mellanlagret
            for i in [0, 1, 2, 3,4,5]:
                for j in [10,11]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-5, 5)))

            # Skapar connections mellan mellan-lagret och output neronen.
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
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []
        for i in range(0, len(self.connections)): # Fyller Node_connections listan
            self.connections[i].from_node.connections.append(self.connections[i])
    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers): # skpar en renad strukturerrad verision av node_listan
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    #Ta ett beslut
    def attention(self,node_upp,node_down):
        """
        Detta är attention blocket, den har till uppgift att skala input-värden baserad på hur relavnt
        den är just nu. Detta görs genom ett mininäterk
        :parameter dem relevanta noderna
        :returns nya ouput värden för dem relevanta noderna
        """
        for i in [6,7,8,9]:
            self.nodes[i].input_value = 0
            self.nodes[i].output_value = 0

        hole_width=(node_upp.output_value+node_down.output_value)

        #Räknar ut y_distansen till hålet.
        number=min(
            [node_upp.output_value,node_upp.output_value])
        if number>0:    y_distance=hole_width/2-number
        elif number<0:  y_distance=hole_width/2+abs(number)
        else:   y_distance=hole_width/2

        # Uppskalning för bättre distenktion mellan värden. (Ju lägre desto högre inlärningstid1)
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
        for i in range(0, self.inputs): #Tömmer
            self.nodes[i].output_value = vision[i]
        self.nodes[5].output_value=1
        self.nodes[12].output_value = 1

        # Innan hela nätverket aktiveras, körs attention algoritmen
        for i in [0,2]:
            self.attention(self.nodes[i],self.nodes[i+1])

        # Nu aktiveras resterande nätverk, men hoppa över samtliga attention-noder
        for i in range(0, len(self.net)):
            if i in [6,7,8,9]:
                pass
            self.net[i].activate()

        output_value = self.nodes[13].output_value

        for i in range(0, len(self.nodes)): #Tömmer
            self.nodes[i].input_value = 0

        return output_value

    # KLona och mutera, för selektion.
    def clone(self):
        clone = Brain(self.inputs, True) #Tom hjärna

        for n in self.nodes: #klona noder
            clone.nodes.append(n.clone())
        for c in self.connections: #klona connections
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers #klona laysers
        clone.generate_net() # Connecta hjärnan ihop.
        return clone
    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n
    def mutate(self, strength,mutation_type):
        for i in range(0, len(self.connections)):
            self.connections[i].mutate_weight(strength,mutation_type)
