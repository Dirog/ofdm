import sys
import json
from PIL import Image
import utils.data as data
from transmitter import Transmitter


if __name__ == '__main__':
    depth = 16
    path = sys.argv[2]
    im = Image.open(path).convert('L')
    im = im.resize((104,130))
    im = im.quantize(colors=depth, method=2)
    image_data = list(im.getdata())
    im.show()

    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)


    print(len(image_data))
    bits = data.bitarray(image_data, depth)

    tx = Transmitter(config)
    tx.transmit(bits)