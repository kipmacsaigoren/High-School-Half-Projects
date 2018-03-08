import numpy
import math
from random import random, randint
import matplotlib.pyplot as plt


with open("/home/kipmacsaigoren/Downloads/train-images-idx3-ubyte", "rb") as rawData:
    rawData.seek(16, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImage = numpy.array([[ord(rawData.read(1)) for i in range(28)] for j in range(28)])

plt.imshow(testImage, cmap='gray')
plt.show()


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Neuron(object):
    def __init__(self, level):
        self.level = level
        self.value = 0
        # to be made random
        if self.level != 0:
            self.bias = randint(-5, 5)
            # to be randomized, the first level has no bias
        self.forwardConnections = {}
        # of the format {neuron:synapse object}
        self.backConnections = {}
        """even though they'll be back connections, the synapse 
        object will be in the same direction if that makes sense.
        like start and end won't be reversed, it will still go from input towards output."""


class Synapse(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = randint(-5, 5)
        # to be randomized


class Network(object):
    def __init__(self, layers):
        if layers != 1:
            self.layers = layers
        else:
            while layers <= 1:
                self.layers = int(input("please choose a number of layers larger than 1"))
        self.neuronsPerLayer = []
        for i in range(layers):
            self.neuronsPerLayer.append(int(input("How many neurons in layer %d?" % i)))
            while self.neuronsPerLayer[i] == 0:
                self.neuronsPerLayer[i] = int(input("please choose a number other than zero"))
        # noinspection PyUnusedLocal
        self.neurons = [[Neuron(j) for i in range(self.neuronsPerLayer[j])] for j in range(layers)]
        for _layer in self.neurons:
            for _neuron in _layer:
                if _neuron.level != layers - 1:
                    # if not in the last layer
                    for i in self.neurons[self.neurons.index(_layer) + 1]:
                        _neuron.forwardConnections[i] = Synapse(_neuron, i)
                if _neuron.level != 0:
                    for i in self.neurons[self.neurons.index(_layer) - 1]:
                        _neuron.backConnections[i] = Synapse(i, _neuron)
        # I think there's something missing in __init__ but we'll have to see.

    # noinspection PyPep8Naming
    def forwardProp(self, data):
        # might be more arguments, who knows
        for i in self.neurons[0]:
            i.value = random()
            # here is where we'll put in the data
        print([j.value for j in self.neurons[0]])
        # PRINT FOR DEBUG
        for layer in range(self.layers):
            # here for seeing the values through the layers
            # noinspection SpellCheckingInspection
            if layer != self.layers - 1:
                weightMatrix = numpy.array(
                    [[i.weight for dummy, i in _neuron.backConnections.items()] for _neuron in self.neurons[layer + 1]])
                """basically i is a neuron in the next level (layer+1) and 
                j is a neuron in the current level (layer) and (i,j) are their coordinates to find
                the weight of their connection in weightMatrix. using weightMatrix[i, j]"""
                valueVector = numpy.array([[i.value] for i in self.neurons[layer]])
                biasVector = numpy.array([[i.bias] for i in self.neurons[layer + 1]])
                newValueVector = numpy.add(numpy.dot(weightMatrix, valueVector), biasVector)
                # HAS NOT been sigmoided yet
                for i in range(self.neuronsPerLayer[layer + 1]):
                    self.neurons[layer + 1][i].value = sigmoid(newValueVector[i][0])
                    # sigmoid it here, might need to be changed later?
                print([j.value for j in self.neurons[layer + 1]])
                # PRINT FOR DEBUG
            else:
                # noinspection PyUnboundLocalVariable
                return newValueVector

