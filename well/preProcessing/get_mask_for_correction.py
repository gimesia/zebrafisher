import numpy as np

from InputImage import InputImage
from well.preProcessing.histc import histc

"""
get a mask for the structured pixels (dart regions (vessels and macula)
and bright regions (papilla)
"""


def get_mask_correction(input_img: InputImage):
    double_img = np.double(input_img.processed)

    # Reshaping the array to (n,1) dimensions... IDK why!
    b_x = double_img.flatten().reshape(-1, 1)
    # Selecting unique values
    b_y = np.unique(b_x).reshape(-1, 1)

    # Histogram bin packing, maybe np.histogram is better
    b_n = histc(b_x, b_y)

    # Removing first element
    b_n = b_n[1:]
    b_y = b_y[1:]

    # Cumulative sum of n
    b_c = np.cumsum(b_n)

    # ?
    b_z = b_c / b_c[-1]

    # Threshold levels
    low_perc = .15
    high_perc = .85

    tl = b_y[np.argwhere(b_z < low_perc)][-1]
    th = b_y[np.argwhere(b_z > high_perc)][0]

    # Creating mask
    xmask = np.zeros(input_img.processed.shape)
    xmask[np.argwhere(
        input_img.processed < tl or input_img.processed > th)] = 1  # xmask(find(input < tl | input > th)) = 1

    mask = np.bwmorph(xmask, 'dilate')  # TODO!

    return mask
