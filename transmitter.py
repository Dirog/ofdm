import time
import numpy as np
import utils.ofdm as ofdm
from utils.sdr import SDR


class Transmitter:
    def __init__(self, config):

        self.fs_hz = config['sampling_rate']
        self.fc_hz = config['carrier_freq']
        self.buffer_size = config['buffer_size']
        self.rx_gain_db = config['rx_gain_dB']
        self.tx_gain_db = config['tx_gain_dB']

        self.fft_size = config['ofdm_fft_size']
        self.carriers = config['ofdm_carriers']
        self.cp_size = config['ofdm_guard_size']
        self.constellation = config['constellation']
        self.pilot_fraction = config['pilot_fraction']
        self.symbols_per_packet = config['symbols_per_packet']

        self.sdr_name = config['tx_device']
        self.sdr = SDR(
            self.sdr_name, self.buffer_size, self.fs_hz, 
            self.fc_hz, self.rx_gain_db, self.tx_gain_db
        )


    def transmit(self) -> None:
        ofdm_tx = ofdm.OFDM(self.fft_size, self.carriers, self.cp_size,
                            self.constellation, self.symbols_per_packet,
                            self.pilot_fraction, self.buffer_size)
        X = 37
        Y = 100
        N = X*Y

        np.random.seed(0)
        tx_data = np.random.choice(self.constellation, (N,)).astype(int)
        packets = ofdm_tx.get_ofdm_packets(tx_data)
        print(packets.shape)
        print(tx_data)

        print('Transmitting!')
        while True:
            for i in range(packets.shape[0]):
                self.sdr.send_data(packets[i,:])
                #time.sleep(0.2)