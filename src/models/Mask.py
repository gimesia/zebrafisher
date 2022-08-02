import numpy as np


class Mask:
    def __int__(self):
        self.og: np.ndarray = None
        self.cropped: np.ndarray = None
        self.masked: np.ndarray = None
        self.cropped_masked: np.ndarray = None

