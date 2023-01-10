import numpy as np


def pow2db(x : float) -> float:
    if x == 0:
        return -np.inf
    x_db = 10.0 * np.log10(x)

    return x_db


def mag2db(x : float) -> float:
    if x == 0:
        return -np.inf
    x_db = 20.0 * np.log10(x)

    return x_db


def db2pow(x_db : float) -> float:
    x = 10.0 ** (x_db / 10.0)

    return x


def db2mag(x_db : float) -> float:
    x = 10.0 ** (x_db / 20.0)

    return x


# Tests
if __name__ == "__main__":
    assert(np.allclose(db2pow(10), 10))
    assert(np.allclose(db2mag(20), 10))
    
    assert(np.allclose(pow2db(1), 0))
    assert(np.allclose(mag2db(1), 0))
    assert(np.allclose(mag2db(0), -np.inf))
    assert(np.allclose(pow2db(0), -np.inf))

    assert(np.allclose(db2mag(mag2db(0)), 0))
    assert(np.allclose(db2mag(mag2db(1.234)), 1.234))
    assert(np.allclose(db2pow(pow2db(4.321)), 4.321))