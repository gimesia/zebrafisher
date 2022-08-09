import numpy as np
from scipy.signal import wiener
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, opening, remove_small_objects, remove_small_holes, binary_dilation
import cv2 as cv

from src.fish import *
from src.models import InputImage, EXAMPLE_IMG
from src.terminal_msg import show_img, msg
from src.well.find_well_props import find_well_props


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")
    # input_img = gaussian_high_pass_filter(input_img)

    input_img = sobel_edges(input_img)

    input_img = yen_thresholding(input_img)

    meniscus = get_meniscus(input_img)
    without_meniscus = input_img.binary
    without_meniscus[meniscus > 0] = 0  # Switching the pixels of the meniscus to 0
    input_img.processed = without_meniscus

    input_img = convex_hull_for_fish(input_img)
    show_img(input_img.fish_props.mask.masked.astype(float))

    # input_img = get_possible_fish(input_img)
    return input_img


if __name__ == '__main__':
    a = InputImage("zf4.jpg")
    a = find_well_props(a)
    a = find_fish_props(a)
