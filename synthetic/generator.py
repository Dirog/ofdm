import numpy as np
from numpy.random import choice


class Generator:
    def __init__(self, buffer_size : int, constel_size : int) -> None:
        self.__buffer_size = buffer_size
        self.__constel_size = constel_size
        self.__global_buffer = []


    def get_symbols(self):
        symbols = choice(self.__constel_size, (self.__buffer_size,))
        symbols = symbols.astype(int)
        self.__global_buffer.append(symbols)
        return symbols


    def get_buffer(self):
        return np.array(self.__global_buffer)