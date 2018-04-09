import numpy
import pickle
import time
from random import shuffle

# feedable format: /home/kipmacsaigoren/Downloads/Training-feed
#    feedable[n] is a 784 element list of gray scale values for nth training image
# printable format: /home/kipmacsaigoren/Downloads/Training-print
#    printable[n] is a 28x28 numpy array with gray scale for nth training image
# labels: /home/kipmacsaigoren/Downloads/Training-labels
#    label[n] is a 10x1 numpy array where correct label = 1 and all other elements are


start = time.time()
with open("/home/kipmacsaigoren/Downloads/neural-net/Training-images", "rb") as L:
    training_feed = pickle.load(L)

with open("/home/kipmacsaigoren/Downloads/neural-net/Training-labels", "rb") as L:
    training_labels = pickle.load(L)

with open("/home/kipmacsaigoren/Downloads/neural-net/Test-images", "rb") as L:
    test_feed = pickle.load(L)

with open("/home/kipmacsaigoren/Downloads/neural-net/Test-labels", "rb") as L:
    test_labels = pickle.load(L)

"""with open("/home/kipmacsaigoren/Downloads/neural-net/Training-print", "rb") as L:
    printImages = pickle.load(L)"""

print("opening took:", time.time()-start)

test_tuples = [(x, y) for x, y in zip(test_feed, test_labels)]

training_tuples = [(x, y) for x, y in zip(training_feed, training_labels)]


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

        """
        INCREDIBLY IMPORTANT: with n layers, there are n-1 weight and bias matrices
        """

    def forward_prop(self, a):
        """might be more arguments, who knows
        data should be in an nx1 numpy vector"""
        for weight, bias in zip(self.weights, self.biases):
            # picks weights from this layer to the next and biases from the next layer
            a = sigmoid(numpy.dot(weight, a) + bias)
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
            error = numpy.multiply(numpy.dot(self.weights[-layer+1].transpose(), error),
                                   sigmoid_prime(z_vectors[-layer]))
            """ wow that was hell to figure out the indices. never using that "self.lengths" shit again
            if I did it with something like "len(self.weights)" plus or minus one, the problem is that
            we need to go back to front and its absolutely impossible to figure out the index on the weights
            
            IMPORTANT FOR UNDERSTANDING: there is no error for the first layer so we don't need the weights
            from layer 1 to 2
            
            A quick explanation:        (W(l) is weights from l to l+1)
            we know error(l) = (W^T(l) * error(l+1))⊙z(l)
            so we want second to last error through error in the second row
            we already have error for the last row, so we start with -2 index.
            this is fine for everything (we already calculated error(l+1) when it was declared)
            but the problem is that weights[-1] is not the weights applied to the last layer
            (which doesn't exist), its the weights from 2nd to last to last layer
            so we add one to the negative weight index so we get the one to the correct row
            
            at the end, we don't calculate an error for the first layer so we don't need the last
            set of weights. that means we can go up to but not including len(self.sizes)
            which would be an index error on self.weights, but that's why we added 1!
            
            jesus christ on two sticks that was so hard to understand.
            """
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
            # So im just using weights without loss of generality
            for i in range(len(self.weights)):
                weight_gradient[i] = weight_gradient[i] + dw[i]
                bias_gradient[i] = bias_gradient[i] + db[i]
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] - \
                              (learning_rate/len(mini_batch))*weight_gradient[i]
            self.biases[i] = self.biases[i] - \
                             (learning_rate/len(mini_batch))*bias_gradient[i]

    def gradient_descent(self, training_data, batch_size, learning_rate, epochs, test_data):
        for i in range(epochs):
            if i == 0:
                tot = 0
                correct = 0
                for inpt, correction in test_data:
                    if self.forward_prop(inpt).argmax() == correction.argmax():
                        correct += 1
                    tot += 1
                print((correct / tot)*100, "% correctly identified")
            shuffle(training_data)
            for j in range(0, len(training_data), batch_size):
                self.update_mini_batch(training_data[j:j+batch_size], learning_rate)
                # update weights and biases for each successive group of [batch_size]
                # sample data and then loop though ever single example
            print("epoch %d completed" % i)
            tot = 0
            correct = 0
            for inpt, correction in test_data:
                if self.forward_prop(inpt).argmax() == correction.argmax():
                    correct += 1
                tot += 1
            print((correct / tot)*100, "% correctly identified")


net = Network([784, 100, 10])
net.gradient_descent(training_tuples, 10, 3.0, 30, test_tuples)


with open("/home/kipmacsaigoren/Downloads/neural-net/Image-classifying-net", "wb") as save:
    pickle.dump(net, save)