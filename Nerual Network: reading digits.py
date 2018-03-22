import numpy
import math
from random import random, randint
import matplotlib.pyplot as plt


with open("/home/kipmacsaigoren/Downloads/train-images-idx3-ubyte", "rb") as rawData:
    rawData.seek(16, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImage = numpy.array([[ord(rawData.read(1)) for i in range(28)] for j in range(28)])


def sigmoid(x):
    return math.exp(x) / (1 + math.exp(x))


arraySig = numpy.vectorize(sigmoid)


class Neuron(object):
    def __init__(self, level):
        self.level = level
        self.value = 0
        # to be made random
        if self.level != 0:
            self.bias = randint(-5, 5)
            # to be randomized, the first level has no bias
        self.forwardConnections = {}
        # of the format {lastLayerNeuron:synapse object} (subject to change)
        self.backConnections = {}
        # {nextLayerNeuron:synapse obj} (subject to change)
        """even though they'll be back connections, the synapse 
        object will be in the same direction if that makes sense.
        like start and end won't be reversed, it will still go from input towards output."""


class Synapse(object):
    # is it necessary?
    # is there a better way to store the weights?
    # maybe instead of neuron.backConnections{lastLayerNeuron:synapse}
    # we can have neuron.backConnections{lastLayerNeuron:weight}
    # that sounds better, just have to make sure we store the
    # same weights for forward and back in the same synapse
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = randint(-2, 2)
        # to be randomized



class Network(object):
    def __init__(self, layers):
        if layers != 1:
            self.layers = layers
        else:
            while layers <= 1 or type(layers) is not int:
                self.layers = int(input("please choose a number of layers larger than 1"))
        self.neuronsPerLayer = [784, 80, 10]
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

    def forwardProp(self, data):
        # might be more arguments, who knows
        for i in range(len(self.neurons[0])):
            self.neurons[0][i].value = data[i//28, i%28]
            # here is where we'll put in the data
        # print([j.value for j in self.neurons[0]])
        # PRINT FOR DEBUG
        for layer in range(self.layers):
            # here for seeing the values through the layers
            if layer != self.layers - 1:
                weightMatrix = numpy.array([[i.weight for dummy, i in _neuron.backConnections.items()] for _neuron in self.neurons[layer + 1]])
                """basically i is a neuron in the next level (layer+1) and 
                j is a neuron in the current level (layer) and (i,j) are their coordinates to find
                the weight of their connection in weightMatrix. using weightMatrix[i, j]"""
                valueVector = numpy.array([[i.value] for i in self.neurons[layer]])
                # column vector of all the values in current layer
                biasVector = numpy.array([[i.bias] for i in self.neurons[layer + 1]])
                # column vector for the biases in the next layer
                newValueVector = numpy.clip(numpy.add(numpy.dot(weightMatrix, valueVector), biasVector), -500, 500)
                # multiplies weightMatrix by valueVector to get unbiased new values then adds biasVector
                # clipped so that sigmoid doesn't produce overflow
                # HAS NOT been sigmoided yet
                for i in range(self.neuronsPerLayer[layer + 1]):
                    self.neurons[layer + 1][i].value = sigmoid(newValueVector[i][0])
                    # I wonder if map works with this
                # print([j.value for j in self.neurons[layer + 1]])
                # PRINT FOR DEBUG
            else:
                # noinspection PyUnboundLocalVariable
                return arraySig(newValueVector)


test = Network(3)
print(test.forwardProp(testImage))

plt.imshow(testImage, cmap='gray')
plt.show()

