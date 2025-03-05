import node
import connection # importerar 2 andra filer och random
import random


class Brain:      # här defineras klassen Brain
    def __init__(self, inputs, clone=False): # den inisiteras klassen med argumenten sig själv inputs och clone som från början är satt som falsk
        self.connections = [] # connections syftar på strecken mellan inputs och bias den sätts som en tom lista
        self.nodes = [] # noderna sätts som en tom lista
        self.inputs = inputs
        self.net = []
        self.layers = 2 # definerar lagrena

        if not clone:
            # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i)) # här "hämtas" Node klassen ur node med argumentet i
                self.nodes[i].layer = 0
            # Create bias node
            self.nodes.append(node.Node(11))
            self.nodes[11].layer = 0
            # Create output node
            self.nodes.append(node.Node(12))
            self.nodes[12].layer = 1

            # Create connections
            for i in range(0, 12):
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[12],
                                                              random.uniform(-1, 1))) # ändrat

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
            self.nodes[i].output_value = vision[i] # Värde för vison är inputsen: från sprite till t.ex övre pipe

        self.nodes[11].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Get output value from output node
        output_value = self.nodes[12].output_value

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
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    # 80 % chance that a connection undergoes mutation
    def mutate(self):
        if random.uniform(0, 1) < 0.4:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()