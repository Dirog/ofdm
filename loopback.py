import sys
import json
from receiver import Receiver
from transmitter import Transmitter
from synthetic.channel import Channel
from synthetic.generator import Generator

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    nsymbols = 3000
    rx = Receiver(config, loopback=True)
    tx = Transmitter(config, loopback=True)
    gen = Generator(nsymbols, config['constellation'])
    ch = Channel()

    symbols = gen.get_symbols()
    ofdm_tx_packets = tx.get_ofdm_packets(symbols)
    
    result = []
    for packet in ofdm_tx_packets:
        ofdm_rx_packet = ch.extend(packet)
        ofdm_rx_packet, _ = ch.add_awgn(ofdm_rx_packet, 3)

        result.append(rx.evaluate(ofdm_rx_packet))

    result = [item for sublist in result for item in sublist]
    print(np.sum(symbols == result[:len(symbols):]) / len(symbols))

    plt.show()