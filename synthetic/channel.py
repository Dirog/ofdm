import numpy as np
from decibels import db2pow
from numpy.random import randn


class Channel:
    def __init__(self) -> None:
        pass


    def add_awgn(self, s, snr_db : float):
        N = len(s)
        snr = db2pow(snr_db)
        n = (randn(N) + 1j*randn(N)) / np.sqrt(2)
        n = n * np.sqrt(np.var(s) / (np.var(n) * snr))

        return s + n, n


    def extend(self, s):
        left = np.random.randint(1, 2000)
        right = np.random.randint(1, 2000)
        s = np.pad(s, (left, right))

        return s


    def __add_delay(self, s, tau : float):
        pass


    def __add_freq_shift(self, s, freq : float):
        pass


# Test
if __name__ == "__main__":
    N = 1000
    snr_db = 10
    snr = db2pow(snr_db)
    s = randn(N) + 1j * randn(N)

    ch = Channel()
    sn, n = ch.add_awgn(s, snr_db)

    measured_snr = np.var(s) / np.var(n)
    assert(np.allclose(measured_snr, snr))