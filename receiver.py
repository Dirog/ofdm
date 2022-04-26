import numpy as np
import utils.ofdm as ofdm
from utils.sdr import SDR


class Receiver:
    def __init__(self, config):

        self.fs_hz = config['sampling_rate']
        self.fc_hz = config['carrier_freq']
        self.buffer_size = config['buffer_size']
        self.rx_gain_db = config['rx_gain_dB']
        self.tx_gain_db = config['tx_gain_dB']

        self.fft_size = config['ofdm_fft_size']
        self.carriers = config['ofdm_carriers']
        self.guard_size = config['ofdm_guard_size']
        self.constellation = config['constellation']
        self.pilot_fraction = config['pilot_fraction']
        self.symbols_per_packet = config['symbols_per_packet']

        self.sdr_name = config['rx_device']
        self.sdr = SDR(
            self.sdr_name, self.buffer_size, self.fs_hz, 
            self.fc_hz, self.rx_gain_db, self.tx_gain_db
            )


    def receive(self):
        temp = ofdm.OFDM(self.fft_size, self.carriers, self.guard_size,
            self.constellation, self.symbols_per_packet, self.pilot_fraction)

        np.random.seed(0)
        X = 37
        Y = 100
        N = X*Y
        true_data = np.random.choice(self.constellation, (N,)).astype(int)
        true_data = np.reshape(true_data, (-1,370))
        print(true_data.flatten())

        for _ in range(10):
            self.sdr.get_data()

        while True:
            raw = self.sdr.get_data()
            status, offset = temp.detect(raw)
            if status and offset < 6000:
                stop = (self.guard_size+self.fft_size)*(self.symbols_per_packet+1)
                raw = raw[offset:offset + stop]
                packet = temp.pipeline(raw)
                for i in range(true_data.shape[0]):
                    ser = 1 - np.mean(packet == true_data[i,:])
                    if ser < 0.50:
                        print(ser, end='\r', flush=True)


