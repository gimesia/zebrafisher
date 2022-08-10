# !!! TODO: UNFINISHED

import numpy as np

from src.models import InputImage
from src.well.unused.histc import histc

"""
get a mask for the structured pixels (dart regions (vessels and macula)
and bright regions (papilla)
"""


def get_mask_for_correction(input_img: InputImage) -> InputImage:
    double_img = np.double(input_img.processed)

    # Reshaping the array to (n,1) dimensions... IDK why!
    b_x = double_img.flatten()  # .reshape(-1, 1)
    # Selecting unique values
    b_y = np.unique(b_x)  # .reshape(-1, 1)

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

    # Last one under & first one over the
    # threshold
    tl = b_y[np.argwhere(b_z < low_perc)][-1][0]
    th = b_y[np.argwhere(b_z > high_perc)][0][0]

    # Creating mask
    mask = np.zeros(input_img.processed.shape)

    # Matlab code ->            xmask(find(input < tl | input > th)) = 1 >>
    # Changing the pixels that don't meet the threshold requirements
    TL = (np.argwhere(input_img.processed < tl))
    TH = (np.argwhere(input_img.processed > th))

    mask[TH] = 1  # TODO ITT A BAJ!!!

    print(mask)

    # mask = np.bwmorph(mask, 'dilate')  # TODO!

    input_img.well_props.mask = mask

    return input_img


if __name__ == "__main__":
    pass