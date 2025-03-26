import node
import connection
import random


class Brain:
    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 3

        if not clone:
            # Skapar perceptroner
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Skapar 3 neuroner i mellanlagret
            for i in [5,6,7]:
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 1
            # Skapar output neuron
            self.nodes.append(node.Node(8))
            self.nodes[8].layer = 2

            # Skapar connections (linjerna med vikter) till mellanlagret
            for i in [0,1,2,3,4]:
                for j in [5,6,7]:
                    self.connections.append(connection.Connection(self.nodes[i],
                                                                  self.nodes[j],
                                                                  random.uniform(-1, 1)))
            # Skapar connections (linjerna med vikter) till output neuron
            for i in [5,6,7]:
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[8],
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

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Få output-värde (y_hat) från output neuron
        output_value = self.nodes[8].output_value

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

    # 80 % chance that a connection undergoes mutation
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
