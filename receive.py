import sys
import json
import numpy as np
import utils.data as data
from receiver import Receiver
import matplotlib.pyplot as plt


if __name__ == '__main__':
    color_depth = 16
    image_size = (104,130)
    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    rx = Receiver(config)
    packets = rx.receive()

    print("Received: {} packets!".format(len(packets)))
    packets = np.array(packets).flatten()
    
    M = config['constellation']
    mod = np.mod(len(packets), M)
    pad = M - mod
    packets = np.pad(packets, (0,pad))
    bits = data.bitarray(packets, M)

    mod = np.mod(len(bits), color_depth)
    pad = color_depth - mod
    bits = np.pad(bits, (0,pad))
    image = data.bits_to_ints(bits, color_depth)

    mod = np.mod(len(image), image_size[1])
    pad = image_size[1] - mod
    image = np.pad(image, (0,pad))
    image = np.reshape(image, (-1, image_size[1]))

    plt.imshow(image)
    plt.show()
    