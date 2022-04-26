import sys
import json
from transmitter import Transmitter


config_path = sys.argv[1]
with open(config_path, 'r') as config_file:
    config = json.load(config_file)


tx = Transmitter(config)
tx.transmit()