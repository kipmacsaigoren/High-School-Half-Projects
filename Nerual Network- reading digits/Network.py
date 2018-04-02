import numpy
import matplotlib.pyplot as plt
import pickle
import time
from random import shuffle

# feedable format: /home/kipmacsaigoren/Downloads/Training-feed
#    feedable[n] is a 784 element list of gray scale values for nth training image
# printable format: /home/kipmacsaigoren/Downloads/Training-print
#    printable[n] is a 28x28 numpy array with gray scale for nth training image
# labels: /home/kipmacsaigoren/Downloads/Training-labels
#    label[n] is a 10x1 numpy array where correct label = 1 and all other elements are 0
start = time.time()
with open("/home/kipmacsaigoren/Downloads/Training-feed", "rb") as L:
    feedForwardImages = pickle.load(L)

with open("/home/kipmacsaigoren/Downloads/Training-print", "rb") as L:
    printImages = pickle.load(L)

with open("/home/kipmacsaigoren/Downloads/Training-labels", "rb") as L:
    feedForwardLabels = pickle.load(L)

print("opening took:", time.time()-start)

training_tuples = [(x, y) for x, y in zip(feedForwardImages, feedForwardLabels)]


def sigmoid(x):
    return 1.0 / (1.0 + numpy.exp(-x))


def sigmoid_prime(x):
    return numpy.exp(-x) / ((1.0 + numpy.exp(-x))**2)


def cost_partial_derivative(output, correction):
    # makes it easier to change up I guess
    return output-correction


class Network(object):
    def __init__(self, sizes):
        self.sizes = sizes
        self.lengths = len(sizes) - 1
        # same as len(biases)==len(weights). used in SGD to avoid zip and confusion
        self.biases = [numpy.random.randn(x, 1) for x in sizes[1:]]
        # makes a random x by 1 vector of biases for all but the input layer
        # with biases[n][m] (or [n][m, 0]) = bias for mth neuron in n+1st layer
        self.weights = [numpy.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        # what the zip does is pick the first element of both, then the second of both, etc
        # so it picks the size for the first layer by the second, then the second by third, etc
        # this way it makes a next-layer-size (y) by this-layer-size (x) matrix of all the weights
        # weights[n][j, i] = weight from neuron i in nth layer to neuron j in n+1st layer

    def forward_prop(self, a):
        """might be more arguments, who knows
        data should be in an nx1 numpy vector"""
        for weight, bias in zip(self.weights, self.biases):
            # picks weights from this layer to the next and biases from the next layer
            a = sigmoid(numpy.clip(numpy.dot(weight, a) + bias, -700, 700))
        return a

    def back_prop(self, inpt, correction):
        """for one input (inpt), and correct classification (correction)
        generates the gradient for all the weights and biases that you can just add
        to the weight and bias matrices"""
        delta_w = []
        delta_b = []
        activation = inpt
        activations = [inpt]
        z_vectors = []
        for weight, bias in zip(self.weights, self.biases):
            z = numpy.dot(weight, activation) + bias
            z_vectors.append(z)
            activation = sigmoid(z)
            activations.append(activation)
            # does the  same thing as forward propagation but saves all the values
            # could it be added in some way to the forward prop function? probably actually
        error = numpy.multiply(cost_partial_derivative(activations[-1], correction),
                               sigmoid_prime(z_vectors[-1]))
        # finds the "error" in each layer of neurons by calculating dC/dZ
        # numpy multiply is element-wise multiplication same as (X*I)*Y where x and y are column vectors
        # starts with the last, output layer of neurons
        delta_b.insert(0, error)
        delta_w.insert(0, numpy.dot(error, activations[-2].transpose()))
        # starting with the second to last layer, going back:
        for layer in range(2, len(self.sizes)):
            error = numpy.multiply(numpy.dot(self.weights[-layer].transpose(), error),
                                   sigmoid_prime(z_vectors[-layer]))
            delta_b.insert(0, error)
            delta_w.insert(0, numpy.dot(error, activations[-layer-1].transpose()))
            # all three taken from here:
            # the same except my layer index for weights is one less than theirs
            # https://i1.wp.com/3bonlp1aiidtbao4s10xacvn-wpengine.netdna-ssl.com/wp-content/uploads/2017/10/tikz21.png?resize=511%2C284&ssl=1
        return delta_w, delta_b

    def update_mini_batch(self, mini_batch, learning_rate):
        """Mini Batch should be a list of tuples in the form
        (input vector, correction vector)
        I use len(self.weights) to as the length of a lot of things be"""
        weight_gradient = [numpy.zeros(w.shape) for w in self.weights]
        bias_gradient = [numpy.zeros(b.shape) for b in self.biases]
        for inpt, correction in mini_batch:
            dw, db = self.back_prop(inpt, correction)
            # len(biases) == len(weights)
            for i in range(self.lengths):
                weight_gradient[i] = weight_gradient[i] + dw[i]
                bias_gradient[i] = bias_gradient[i] + db[i]
        for i in range(self.lengths):
            self.weights[i] = self.weights[i] - \
                              (learning_rate/len(mini_batch))*weight_gradient[i]
            self.biases[i] = self.biases[i] - \
                             (learning_rate/len(mini_batch))*bias_gradient[i]

    def gradient_descent(self, training_data, batch_size, learning_rate, epochs, test_data):
        for i in range(epochs):
            shuffle(training_data)
            for j in range(0, len(training_data), batch_size):
                self.update_mini_batch(training_data[j:j+batch_size], learning_rate)
                # update weights and biases for each successive group of [batch_size]
                # sample data and then loop though ever single example

            print("epoch %d completed" %i)


net = Network([784, 15, 10])

