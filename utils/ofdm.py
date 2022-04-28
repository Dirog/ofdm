import numpy as np
import utils.qam as qam
import scipy.signal as sp
import utils.debug as debug


class OFDM:
    def __init__(self, fft_size : int, carriers : int, cp_size : int,
                 mod_oder : int, symbols_per_packet : int,
                 pilot_fraction : int, buffer_size : int) -> None:

        self.symbols_per_packet = symbols_per_packet
        self.buffer_size = buffer_size
        self.fft_size = fft_size
        self.carriers = carriers
        self.cp_size = cp_size

        self.stf = self.__generate_stf()
        self.constellation = qam.constellation(mod_oder)

        self.acf_threshold = 0.8

        self.pilot_fraction = pilot_fraction
        self.pilot_count = int(self.carriers * self.pilot_fraction)
        self.pilots, self.pilot_indexes, self.info_indexes = self.__get_pilots()

        max_acf_index = self.buffer_size - self.cp_size - self.fft_size
        symbols_len = (self.fft_size + self.cp_size) * self.symbols_per_packet
        self.max_offset = max_acf_index - len(self.stf) - symbols_len


    def modulate(self, iq : np.array(np.complex64)) -> np.array(np.complex64):
        pad = (self.fft_size - self.carriers) // 2
        iq = np.reshape(iq, (-1, self.carriers))
        iq = np.pad(iq, ((0, 0), (pad, pad)))
        iq = np.fft.fftshift(iq, axes=(1,))

        return np.fft.ifft(iq, self.fft_size)


    def demodulate(self, x : np.array(np.complex64)) -> np.array(np.complex64):
        iq = np.fft.fft(x, self.fft_size)
        iq = np.fft.fftshift(iq, axes=(1,))

        pad = (self.fft_size - self.carriers) // 2
        return iq[:, pad:self.fft_size - pad]


    def insert_pilots(self, iq_info: np.array(np.complex64)) -> np.array(np.complex64):
        iq = np.zeros((iq_info.shape[0], self.carriers), dtype=np.complex64)
        iq[:, self.pilot_indexes] = self.pilots
        iq[:, self.info_indexes] = iq_info

        return iq


    def insert_cyclic_prefix(self, x : np.array(np.complex64)) -> np.array(np.complex64):
        N = x.shape[1]
        y = np.zeros((x.shape[0], x.shape[1] + self.cp_size), dtype=np.complex64)
        y[:, :self.cp_size] = x[:, N - self.cp_size:N:]
        y[:, self.cp_size:] = x

        return y


    def remove_cyclic_prefix(self, y):
        x = np.zeros((y.shape[0], y.shape[1] - self.cp_size), dtype=np.complex64)
        x = y[:, self.cp_size::]

        return x


    def acf(self, x : np.array(np.complex64), width : int, step : int) -> np.array(np.complex64):
        x += 1e-30 + 1j * 1e-30
        acf = np.zeros((len(x) - width - step,), dtype=complex)
        for i in range(len(acf)):
            lhs = x[i:i+width]
            rhs = x[i+step:i+step+width]
            norm = np.sqrt(np.vdot(lhs,lhs) * np.vdot(rhs,rhs))
            acf[i] = np.vdot(lhs, rhs) / norm

        return acf


    def get_ofdm_packets(self, symbols : np.array(int)) -> np.array(np.complex64):
        iq = qam.modulate(symbols, self.constellation)
        iq = np.reshape(iq, (-1, self.carriers - self.pilot_count))
        iq = self.insert_pilots(iq)

        signal = self.modulate(iq)
        signal = self.insert_cyclic_prefix(signal)
        packets = np.reshape(signal, (-1, (self.fft_size+self.cp_size) * self.symbols_per_packet))
        prefixes = np.tile(self.stf, (packets.shape[0], 1))
        packets = np.concatenate((prefixes, packets), axis=1)

        print("Ready to transmit {} OFDM packets with {} samples each."
                .format(packets.shape[0], packets.shape[1]))

        return packets


    def equalize(self, iq : np.array(np.complex64)) -> np.array(np.complex64):
        rx_pilots = iq[:, self.pilot_indexes]
        ch_estimate = rx_pilots / self.pilots

        channel = []
        iq_equalized = np.zeros(iq.shape, dtype=np.complex64)
        n = np.arange(self.carriers)
        for i in range(iq.shape[0]):
            temp = np.interp(n, self.pilot_indexes, ch_estimate[i, :])
            iq_equalized[i, :] = (iq[i, :] / (temp + 1e-20))
            channel.append(temp)

        if __debug__:
            debug.plot_channel(np.abs(np.array(channel)))

        return iq_equalized[:, self.info_indexes]


    def pipeline(self, raw : np.array(np.complex64)) -> np.array(int):
        symbols = self.sync(raw)
        iq = self.demodulate(symbols)
        iq_info = self.equalize(iq)
        iq_info = iq_info.flatten()

        if __debug__:
            debug.plot_constellation(iq_info)

        return qam.demodulate(iq_info, self.constellation)


    def detect(self, raw : np.array(np.complex64)) -> bool:
        corr = self.acf(raw, 16, 16)
        corr_abs = self.__moving_average(np.abs(corr), 32)

        if __debug__:
            debug.plot_acf_and_psd(raw, corr_abs)

        mask = corr_abs > self.acf_threshold
        if any(mask):
            offset = np.max(np.nonzero(mask))
            return True, offset

        return False, None


    def sync(self, raw : np.array(np.complex64)) -> np.array(np.complex64):
        corr = self.acf(raw, self.cp_size, self.fft_size)
        corr_abs = np.abs(corr)

        peaks, _ = sp.find_peaks(corr_abs, height=self.acf_threshold, 
                    distance=self.fft_size+self.cp_size-4)

        if __debug__:
            debug.plot_acf(corr_abs, peaks)

        symbols = np.ones((len(peaks), self.fft_size), dtype=np.complex64)
        if len(peaks) != self.symbols_per_packet:
            #print(len(peaks), end='\r', flush=True)
            return symbols

        STO = peaks
        CFO = 1 / (2*np.pi) * np.angle(corr[peaks])

        n = np.arange(0, self.fft_size)
        for i in range(len(peaks)):
            start = STO[i] + self.cp_size
            symbol = raw[start: start + self.fft_size]
            shift = np.exp(-1j * 2 * np.pi * CFO[i] * n / self.fft_size)
            symbols[i, :] = symbol * shift

        return symbols

    
    def __moving_average(self, x : np.array, w : int) -> np.array:
        return np.convolve(x, np.ones(w), 'valid') / w


    def __get_pilots(self) -> np.array(np.complex64):
        pilot_indexes = np.linspace(0, self.carriers-1, self.pilot_count).astype(int)

        indexes = np.arange(0, self.carriers)
        info_indexes = np.setxor1d(indexes, pilot_indexes)
        
        pilots = np.zeros((self.pilot_count,), dtype=np.complex64)
        for i in range(self.pilot_count):
            pilots[i] = (2 * np.mod(i,2) - 1) * (1+1j)

        return pilots, pilot_indexes, info_indexes


    def __generate_stf(self) -> np.array(np.complex64):
        ampl = np.sqrt(13 / 6)
        seq = np.array(
            [0,0,
            +1+1j,0,0,0,-1-1j,0,0,0,
            +1+1j,0,0,0,-1-1j,0,0,0,
            -1-1j,0,0,0,+1+1j,0,0,0,
            0,0,0,0,
            -1-1j,0,0,0,-1-1j,0,0,0,
            +1+1j,0,0,0,+1+1j,0,0,0,
            +1+1j,0,0,0,+1+1j
            ,0,0]
            )

        seq = np.pad(seq, (6,6))
        stf = np.fft.ifft(ampl * seq, 64)
        stf = np.tile(stf, 2)
        stf = np.concatenate((stf[-32:], stf, [stf[-32]]))
        stf[0] *= 0.5; stf[-1] *= 0.5
        return stf