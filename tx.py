import sys
import json
from utils.sdr import SDR
from transmitter import Transmitter
from synthetic.generator import Generator


if __name__ == "__main__":
    config_path = sys.argv[1]
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    nsymbols = 1000000
    tx = Transmitter(config)
    gen = Generator(nsymbols, config['constellation'])

    sdr = SDR(
        config['tx_device'], config['buffer_size'], config['sampling_rate'], 
        config['carrier_freq'], config['rx_gain_dB'], config['tx_gain_dB']
        )

    symbols = gen.get_symbols()
    ofdm_tx_packets = tx.get_ofdm_packets(symbols)

    for packet in ofdm_tx_packets:
        sdr.send_data(packet)