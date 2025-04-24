import node
import connection
import random

class Brain:
    def __init__(self, inputs, clone=False):
        # initierar hjärnan med startdvärdet, baserat på om det är en klon. 
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Create bias node
            self.nodes.append(node.Node(5))
            self.nodes[3].layer = 0
            # Create output node
            self.nodes.append(node.Node(6))
            self.nodes[4].layer = 1

            # Create connections
            for i in range(0, 4):
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[4],
                                                              random.uniform(-3, 3)))

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

        self.nodes[3].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Get output value from output node

        output_value = self.nodes[4].output_value


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
        # Denna funktion kan bara tillgås genom nya gentiska spelare och kris mutaion.
        # Så type är antigen 1 eller 2
        for i in range(0, len(self.connections)):
            self.connections[i].mutate_weight(strength,mutation_type)

