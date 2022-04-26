import numpy as np
from math import log


def modulate(x, constel):
    return constel[x]


def demodulate(x, constel):
    samples = len(x)
    result = np.zeros(x.shape)
    for i in range(samples):
        j = np.argmin(np.abs(constel - x[i]))
        result[i] = j
    
    return result.astype(int)


def norm(constel):
    dot = np.dot(constel, np.conj(constel))
    return constel / np.abs(np.sqrt(dot / len(constel)))


def constellation(M):
    if M == 2:
        return norm(np.array([-1,1]))
    if np.fix(log(M, 4)) != log(M,4):
        raise ValueError("M must be 2 or power of 4!")

    nbits = int(np.log2(M))
    x = np.arange(M)

    nbitsBy2 = nbits >> 1
    symbolI = x >> nbitsBy2
    symbolQ = x & ((M-1) >> nbitsBy2)

    i = 1
    while i < nbitsBy2:
        tmpI = symbolI
        tmpI = tmpI >> i
        symbolI = symbolI ^ tmpI

        tmpQ = symbolQ
        tmpQ = tmpQ >> i
        symbolQ = symbolQ ^ tmpQ
        i = i + i

    gray = (symbolI << nbitsBy2) + symbolQ

    x = x[gray]
    c = int(np.sqrt(M))
    I = -2 * np.mod(x, c) + c - 1
    Q = 2 * np.floor(x / c) - c + 1
    IQ = I + 1j*Q
    IQ = -np.transpose(np.reshape(IQ, (c, c)))
    return norm(IQ.flatten())


# Test
if __name__ == "__main__":
    M = 16
    N = 100
    x = np.random.choice(M, (N,)).astype(int)
    
    constel = constellation(M)
    y = modulate(x, constel)
    z = demodulate(y, constel)

    assert(np.sum(x == z) == N)