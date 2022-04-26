import numpy as np
import matplotlib.pyplot as plt


def plot_acf_and_psd(raw, acf):
    plt.figure(1)
    plt.subplot(2,2,1)
    plt.cla()
    plt.plot(np.abs(acf))
    plt.title('Packet ACF')
    plt.xlabel('n')
    plt.ylim([0,1.1])
    plt.grid()

    plt.subplot(2,2,2)
    plt.cla()
    plt.psd(raw, NFFT=1024)
    plt.tight_layout()
    plt.pause(0.01)
    #plt.show()


def plot_constellation(iq):
    plt.figure(1)
    plt.subplot(2,2,4)
    plt.cla()
    plt.scatter(np.real(iq), np.imag(iq), alpha=0.5)
    plt.title('Signal constellation')
    plt.xlim([-1.5,1.5])
    plt.ylim([-1.5,1.5])
    plt.xlabel('I')
    plt.ylabel('Q')
    plt.grid()
    plt.pause(0.01)


def plot_acf(acf, peaks):
    plt.figure(1)
    plt.subplot(2,2,3)
    plt.cla()
    plt.plot(np.abs(acf))
    plt.plot(peaks, np.abs(acf[peaks]), marker='x')
    plt.title('Symbols ACF')
    plt.xlabel('n')
    plt.ylim([0,1.1])
    plt.xlim([0,1800])
    plt.grid()
    plt.pause(0.01)

