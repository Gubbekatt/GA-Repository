import node
import connection
import random


class Brain:
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
            # Skapar bias
            self.nodes.append(node.Node(5))
            self.nodes[5].layer = 0
            # Skapar 3 neuroner i mellanlager 1
            for i in range[6,7,8]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 1
            # Skapar bias
            self.nodes.append(node.Node(9))
            self.nodes[9].layer = 1
            # Skapar 2 neuroner i mellanlager 2
            for i in [10,11]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 2
            # Skapar bias
            self.nodes.append(node.Node(12))
            self.nodes[12].layer = 2
            # Skapar output neuron
            self.nodes.append(node.Node(13))
            self.nodes[13].layer = 3

            # Skapar connections (linjerna med vikter) till mellanlager 1 och bias
            for i in [0,1,2,3,4,5]:
                for j in [6,7,8]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-1, 1)))

            # Skapar connections (linjerna med vikter) till mellanlager 2 och bias
            for i in [6,7,8,9]:
                for j in [10,11]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-1, 1)))

            # Skapar connections (linjerna med vikter) till output neuron och bias
            for i in [10,11,12]:
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[13],
                                                              random.uniform(-1, 1)))

    def connect_nodes(self):
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

    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[5].output_value = 1
        self.nodes[9].output_value = 1
        self.nodes[12].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Få output-värde (y_hat) från output neuron
        output_value = self.nodes[13].output_value

        # Reset input neuroner (perceptroner)
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value

    def clone(self):
        clone = Brain(self.inputs, True)

        # Klonar alla neuroner
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Klonar alla connections (linjer med vikter)
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    def mutate(self, strength,mutation_type):
        # Denna funktion kan bara tillgås genom nya gentiska spelare och kris mutaion.
        # Så type är antigen 1 eller 2
        for i in range(0, len(self.connections)):
            self.connections[i].mutate_weight(strength,mutation_type)
