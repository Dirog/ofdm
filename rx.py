import sys
import json
from receiver import Receiver


config_path = sys.argv[1]
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

rx = Receiver(config)
print('Testing!')
rx.receive()