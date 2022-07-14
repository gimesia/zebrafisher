# !!! TODO: UNFINISHED

import numpy as np

from InputImage import InputImage


def robust_homomorphic_surface_fitting(input_img: InputImage, mask: np.ndarray) -> InputImage:
    gd = input_img.processed
    gd[mask] = 0 # Már itt rossz

    return input_img
