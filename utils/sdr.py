import adi
import numpy as np
#import utils.libhackrf as libhackrf

class SDR:
    def __init__(self, sdr_name, buffer_size, fs_hz, central_freq, rx_gain_db, tx_gain_db):
        self.central_freq = central_freq
        self.buffer_size = buffer_size
        self.rx_gain_db = rx_gain_db
        self.tx_gain_db = tx_gain_db
        self.sdr_name = sdr_name
        self.fs_hz = fs_hz

        if sdr_name == 'pluto':
            try:
                pluto_ip = "ip:192.168.2.1"
                self.sdr = adi.Pluto(pluto_ip)
            except:
                raise Exception("Cannot init Pluto device!")

            self.sdr.gain_control_mode_chan0 = 'manual'
            self.sdr.rx_hardwaregain_chan0 = self.rx_gain_db
            self.sdr.tx_hardwaregain_chan0 = self.tx_gain_db
            self.sdr.rx_lo = int(self.central_freq)
            self.sdr.tx_lo = int(self.central_freq)
            self.sdr.sample_rate = int(self.fs_hz)
            self.sdr.rx_rf_bandwidth = int(self.fs_hz)
            self.sdr.tx_rf_bandwidth = int(self.fs_hz)
            self.sdr.rx_buffer_size = buffer_size
            self.sdr.tx_destroy_buffer()
        elif sdr_name == 'hackrf':
            try:
                self.sdr = libhackrf.HackRF()
            except:
                raise Exception("Cannot init HackRF device!")

            self.sdr.sample_rate = self.fs_hz
            self.sdr.center_freq = self.central_freq
            #TODO create variables for gains
            self.sdr.set_vga_gain(24)
            self.sdr.set_lna_gain(34)


    def get_data(self):
        if self.sdr_name == 'pluto':
            return self.sdr.rx()
        elif self.sdr_name == 'hackrf':
            return self.sdr.read_samples(self.buffer_size)


    def send_data(self, packet):
        self.sdr._tx_buffer_size = int(2**18)
        packet /= np.max(np.abs(packet))
        self.sdr.tx(packet * 2**14)
        self.sdr.tx_destroy_buffer()


    def clear_rx(self):
        if self.sdr_name == 'pluto':
            self.sdr.rx_destroy_buffer()
        for _ in range(5):
            self.get_data()


    def set_central_freq(self, freq):
        self.central_freq = freq
        self.sdr.rx_lo = int(self.central_freq)
        print("Changed central freq to {}MHz!".format(freq / 1e6))

