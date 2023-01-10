import time
import numpy as np
import utils.ofdm as ofdm
#from utils.sdr import SDR


class Transmitter:
    def __init__(self, config, loopback=False):

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

        self.__ofdm = ofdm.OFDM(self.fft_size, self.carriers, self.cp_size,
                            self.constellation, self.symbols_per_packet,
                            self.pilot_fraction, self.buffer_size
                            )




    def get_ofdm_packets(self, symbols):
        return self.__ofdm.get_ofdm_packets(symbols)
        