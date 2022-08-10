import numpy as np
from skimage.color import label2rgb
from skimage.measure import find_contours

from src.fish import *
from src.models import InputImage, EXAMPLE_IMG
from src.terminal_msg import show_img, msg
from src.well.find_well_props import find_well_props


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")
    # input_img = gaussian_high_pass_filter(input_img)



    input_img = sobel_edges(input_img)

    input_img = yen_thresholding(input_img)

    input_img = remove_meniscus(input_img)

    input_img = convex_hull_for_fish(input_img)
    show_img(input_img.processed)

    if input_img.fish_props.mask.og.nonzero()[0].size > input_img.well_props.mask.cropped_masked.nonzero()[0].size * 0.5:
        show_img(input_img.fish_props.mask.og)
        # input_img = correct_fish_mask(input_img)

    return input_img


if __name__ == '__main__':
    a = InputImage("zf1.jpg")
    a = find_well_props(a)
    a = find_fish_props(a)
