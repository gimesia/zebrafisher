import numpy as np

from InputImage import InputImage
from well.preProcessing.histc import histc

"""
get a mask for the structured pixels (dart regions (vessels and macula)
and bright regions (papilla)
"""


def get_mask_correction(input_img: InputImage):
    double_img = np.double(input_img.processed)

    # Reshaping the array, IDK why!
    b_x = double_img.reshape((double_img.shape[0] * double_img.shape[1]), 1);

    b_y = np.unique(b_x);
    b_n = histc(b_x, b_y);

    ## ITT TARTOTTAM
    b_n[0] = [];
    b_y[0] = [];
    b_c = np.cumsum(b_n);
    b_z = b_c / b_c[-1];

    low_perc = .15;
    high_perc = .85;

    TL = b_y(find(b_z < low_perc, 1, 'last'));
    TH = b_y(find(b_z > high_perc, 1, 'first'));

    Xmask = np.zeros(input_img.processed.shape);
    Xmask(find(input < TL | input > TH)) = 1;
    Xmask2 = bwmorph(Xmask, 'dilate');

    return Xmask2;
