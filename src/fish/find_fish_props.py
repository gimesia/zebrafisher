import numpy as np
from scipy.signal import wiener
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, opening, remove_small_objects, remove_small_holes, binary_dilation
import cv2 as cv

from src.fish.get_possible_fish import get_possible_fish
from src.fish.guassian_hpf import gaussian_high_pass_filter
from src.fish.yen_thresholding import yen_thresholding
from src.models import InputImage, EXAMPLE_IMG
from src.terminal_msg import show_img, msg
from src.well.find_well_props import find_well_props


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")
    filtered_img = input_img.processed

    input_img = gaussian_high_pass_filter(input_img)
    show_img(input_img.processed)


    # input_img = yen_thresholding(input_img)

    thresh = threshold_yen(input_img.processed)
    binary = np.zeros(input_img.processed.shape, dtype=int)
    binary[np.where(input_img.processed > thresh)] = 1
    show_img(binary)

    dilated = binary_dilation(input_img.binary)
    input_img.processed = dilated

    min_size = input_img.well_props.mask.cropped_masked.size * 0.1

    removed_objects_and_holes = input_img.binary.copy()

    """removed_objects_and_holes = remove_small_objects(
        remove_small_holes(removed_objects_and_holes, connectivity=np.ndim(removed_objects_and_holes)))"""

    # filtered_img = wiener(input_img.processed, (5, 5))
    # input_img = get_possible_fish(input_img)

    show_img(removed_objects_and_holes.astype(int))
    return input_img


if __name__ == '__main__':
    a = EXAMPLE_IMG
    a = find_well_props(a)
    a = find_fish_props(a)
