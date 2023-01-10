import sys
import json
from utils.sdr import SDR
from receiver import Receiver

if __name__ == "__main__":
    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    rx = Receiver(config)
    sdr = SDR(
        config['tx_device'], config['buffer_size'], config['sampling_rate'], 
        config['carrier_freq'], config['rx_gain_dB'], config['tx_gain_dB']
        )

    while True:
        packet = sdr.get_data()
        rx.evaluate(packet)