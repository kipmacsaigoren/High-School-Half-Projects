import pickle
import matplotlib.pyplot as plt
import numpy

# pixel data is divided by 255 to prevent overflow. i think I should still work

with open("/home/kipmacsaigoren/Downloads/neural-net/train-images-idx3-ubyte", "rb") as rawData:
    rawData.seek(16, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImages = [numpy.array([[ord(rawData.read(1))/255.0] for i in range(784)]) for j in range(60000)]
    with open("/home/kipmacsaigoren/Downloads/neural-net/Training-images", "wb") as saveFile:
        pickle.dump(testImages, saveFile)

with open("/home/kipmacsaigoren/Downloads/neural-net/train-labels-idx1-ubyte", "rb") as rawData:
    rawData.seek(8, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImages = []
    for i in range(60000):
        label = ord(rawData.read(1))
        e = numpy.zeros((10, 1))
        e[label] = 1.0
        testImages.append(e)
    with open("/home/kipmacsaigoren/Downloads/Training-labels", "wb") as saveFile:
        pickle.dump(testImages, saveFile)

with open("/home/kipmacsaigoren/Downloads/neural-net/t10k-images-idx3-ubyte", "rb") as rawData:
    rawData.seek(16, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImages = [numpy.array([[ord(rawData.read(1))/255.0] for i in range(784)]) for j in range(10000)]
    with open("/home/kipmacsaigoren/Downloads/neural-net/Test-images", "wb") as saveFile:
        pickle.dump(testImages, saveFile)

with open("/home/kipmacsaigoren/Downloads/neural-net/t10k-labels-idx1-ubyte", "rb") as rawData:
    rawData.seek(8, 1)
    # 28x28 pixels
    # the first 16 bytes are header stuff
    testImages = []
    for i in range(10000):
        label = ord(rawData.read(1))
        e = numpy.zeros((10, 1))
        e[label] = 1.0
        testImages.append(e)
    with open("/home/kipmacsaigoren/Downloads/Test-labels", "wb") as saveFile:
        pickle.dump(testImages, saveFile)

