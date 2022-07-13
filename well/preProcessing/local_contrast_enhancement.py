import numpy as np
from scipy.signal import convolve2d

from InputImage import InputImage

"""
TODO! körbepisilni a témát még egy kicsit -> roifilt2(), fspecial('average')
"""


def local_contrast_enhancement(input_img: InputImage):
    double = np.double(input_img.processed) / 255

    imgtype = 1
    subsamplingrate = 1

    mask = np.zeros(double.shape)
    print(mask)
    print(mask.shape)

    # Putting 1s in first and last row
    mask[:1, :] = 1
    mask[-1:, :] = 1

    # Putting 1s in first and last col
    mask[:, -1:] = 1
    mask[:, :1] = 1

    se_size3 = 35

    # The best solution for the following line
    # muf = roifilt2(fspecial('average', se_size3), f, 1 - mask);

    return input_img


if __name__ == "__main__":
    pass
