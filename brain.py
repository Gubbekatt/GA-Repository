import node
import connection
import random


class Brain:      # här definieras klassen Brain
    def __init__(self, inputs, clone=False): # den initierar vi klassen med argumenten sig själv inputs och clone som från början är satt som falsk
        self.brain_connections = [] # connections syftar på strecken mellan inputs och bias den sätts som en tom lista
        self.nodes = [] # noderna sätts som en tom lista
        self.inputs = inputs # antalet saker fågeln ser
        self.net = [] # alla noder sorterade efter ordningen de dyker upp i, alltså först input, sist output
        self.layers = 4 #2 # definierar antalet lager

        if not clone:
            # Skapar input noder
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i)) # här "hämtas" Node klassen ur node med argumentet i
                self.nodes[i].layer = 0
            # Skapar bias nod i lager 1
            self.nodes.append(node.Node(12))
            self.nodes[12].layer = 0
            # Skapar första mellan-lagret
            for i in range(0, 4):
                self.nodes.append(node.Node(i+len(self.nodes)))
                self.nodes[i+len(self.nodes)].layer = 1
            # Skapar lager 2 bias
            self.nodes.append(node.Node(17))
            self.nodes[17].layer = 1
            # Skapar andra mellan-lagret
            for i in range(0, 2):
                self.nodes.append(node.Node(i+len(self.nodes)))
                self.nodes[i+len(self.nodes)].layer = 2
            # Skapar lager 3 bias
            self.nodes.append(node.Node(20))
            self.nodes[20].layer = 2
            # Skapar output nod
            self.nodes.append(node.Node(21))
            self.nodes[21].layer = 3

            # Skapar connections
    # weight_list = []
            # den ser 12 saker och har en bias i första lagret = 13 noder
            # for i in range(0, 13):
            #     # Appends
            #     self.brain_connections.append(connection.Connection(self.nodes[i],
            #                                                         self.nodes[13],
            #                                                         random.uniform(-1,1)))#weight_list[i])) # ändrat

            # Första mellanlagret
            # Skickar de två första inputen och skapar den första noden
            self.brain_connections.append(connection.Connection(self.nodes[1],
                                                            self.nodes[13],
                                                            random.uniform(-1,1)))
            self.brain_connections.append(connection.Connection(self.nodes[2],
                                                                self.nodes[13],
                                                                random.uniform(-1, 1)))
            # Skapar nod 2
            for i in range(4, 6):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[14],
                                                                    random.uniform(-1, 1)))
            # Skapar nod 3
            for i in range(6,8):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[15],
                                                                    random.uniform(-1, 1)))
            # Ger mellan-lager 1,2 & 3 vetskap om distans i x-led till röret från fågelns fram- och bakdel
            for i in range(1,3):
                for j in range(13, 16):
                    self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                self.nodes[j],
                                                                random.uniform(-1, 1)))
            # Skapar hinder-noden i mellan-lager 1
            for i in range(8, 12):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[16],
                                                                    random.uniform(-1, 1)))
            # Skapar bias i mellan-lager 1
            for i in range(13,17):
                self.brain_connections.append(connection.Connection(self.nodes[12],
                                                                    self.nodes[i],
                                                                    random.uniform(-1, 1)))

            # Andra mellan-lagret
            # Skapar 1-2 hål noden
            for i in range(13,15):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[18],
                                                                    random.uniform(-1, 1)))
            # Skapar 2-3 hål noden
            for i in range(14,16):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[19],
                                                                    random.uniform(-1, 1)))
            # Ger både nod 1 & 2 i mellanlager 2 vetskap om hindret
            for i in range(18,20):
                self.brain_connections.append(connection.Connection(self.nodes[16],
                                                                    self.nodes[i],
                                                                    random.uniform(-1, 1)))
            # Ger både nod 1 & 2 i mellanlager 2 bias
            for i in range(18,20):
                self.brain_connections.append(connection.Connection(self.nodes[17],
                                                                    self.nodes[i],
                                                                    random.uniform(-1, 1)))
            # Output
            for i in range(18,21):
                self.brain_connections.append(connection.Connection(self.nodes[i],
                                                                    self.nodes[21],
                                                                    random.uniform(-1, 1)))


    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.brain_connections)):
            self.brain_connections[i].from_node.brain_connections.append(self.brain_connections[i])

    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i] # Värde för vison är inputsen: från sprite till t.ex övre pipe

        self.nodes[12].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Get output value from output node
        output_value = self.nodes[13].output_value

        # Reset node input values - only node 6 Missing Natural Selection in this case
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value

    def clone(self):
        clone = Brain(self.inputs, True)

        # Clone all the nodes
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Clone all connections
        for c in self.brain_connections:
            clone.brain_connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    # 80 % chance that a connection undergoes mutation
    def mutate(self):
        if random.uniform(0, 1) < 0.4:
            for i in range(0, len(self.brain_connections)):
                self.brain_connections[i].mutate_weight()