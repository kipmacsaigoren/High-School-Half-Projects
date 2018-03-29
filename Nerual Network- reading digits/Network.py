import numpy
import matplotlib.pyplot as plt
import pickle
from os.path import isfile

# feedable format: /home/kipmacsaigoren/Downloads/Training-feed
#    feedable[n] is a 784 element list of gray scale values for nth training image
# printable format: /home/kipmacsaigoren/Downloads/Training-print
#    printable[n] is a 28x28 numpy array with gray scale for nth training image
# labels: /home/kipmacsaigoren/Downloads/Training-labels
#    label[n] is an integer labeling the nth training image


def sigmoid(x):
    return 1.0 / (1.0 + numpy.exp(-x))


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

