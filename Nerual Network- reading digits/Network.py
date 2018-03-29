import numpy
import matplotlib.pyplot as plt
import pickle
from os.path import isfile

# test data in feedable format: /home/kipmacsaigoren/Downloads/Training-feed
#    feedable[n] is a 784 element list of gray scale values for nth training image
# test data in printable format: /home/kipmacsaigoren/Downloads/Training-print
#    printable[n] is a 28x28 numpy array with gray scale for nth training image
# labels: /home/kipmacsaigoren/Downloads/Training-labels
#    label[n] is an integer labeling the nth training image


"""with open("/home/kipmacsaigoren/Downloads/train-images-idx3-ubyte", "rb") as rawData:
    rawData.seek(16, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImagesToPrint = [numpy.array([[ord(rawData.read(1)) for i in range(28)] for j in range(28)]) for k in range(60000)]
"""


def sigmoid(x):
    return 1.0 / (1.0 + numpy.exp(-x))


"""
class Neuron(object):
    # Ha ha it turns out this is even also not necessary
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
        even though they'll be back connections, the synapse 
        object will be in the same direction if that makes sense.
        like start and end won't be reversed, it will still go from input towards output.


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
"""

class Network(object):
    def __init__(self, sizes):
        self.sizes = sizes
        self.biases = [numpy.random.randn(x, 1) for x in sizes[1:]]
        # makes a random x by 1 vector of biases for all but the input layer
        # with biases[n][m] (or [n][m, 0]) = bias for mth neuron in n+1st layer
        self.weights = [numpy.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        # what the zip does is pick the first element of both, then the second of both, etc
        # so it picks the size for the first layer by the second, then the second by third, etc
        # this way it makes a next-layer-size (y) by this-layer-size (x) matrix of all the weights
        # weights[n][j, i] = weight from neuron i in nth layer to neuron j in n+1st layer

    def forward_prop(self, a):
        # might be more arguments, who knows
        # data should be in an nx1 numpy vector
        for w, b in zip(self.weights, self.sizes):
            # picks weights from this layer to the next and biases from the next layer
            a = sigmoid(numpy.dot(w, a) + b)
        return a


test = Network([784, 15, 10])
#print(test.forward_prop([testImages[3]]))
plt.imshow(testImagesToPrint[3], cmap='gray')
plt.show()

