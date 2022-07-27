import numpy as np
import scipy
from skimage import measure, filters, morphology
from skimage.morphology import disk, closing

from src.InputImage import InputImage, Mask
from src.fish.get_possible_fish import modify_circle, get_objects, is_fish, get_plate_width_and_remove_sides
from src.well.is_empty_img import is_empty_img


def get_possible_fish(input_img: InputImage):
    """
    Returns the sum of two decimal numbers in binary digits.

        Parameters:
                input_img (InputImage): Input Image

        Returns:
                output_img (InputImage):
    """
    well_cropped_gray = input_img.well_props.mask.cropped_gray

    segmented_fish_size_first = np.zeros_like(input_img.og)
    segmented_fish_size_second = np.zeros_like(input_img.og)

    crop_mask = input_img.well_props.mask.cropped
    binary_img = input_img.binary

    # input_img.cont = bwperim(crop_mask);
    # binary_img = bwareaopen(binary_img, 100)

    input_img.fish_props.container = measure.perimeter(input_img.well_props.mask.cropped)  # Ez nem jó
    binary_img = morphology.area_opening(input_img.processed, 100)

    thresholded_mask = get_plate_width_and_remove_sides(,, False)
    input_img.fish_props.mod_cont = thresholded_mask

    binary_img[np.where(thresholded_mask > 0)] = 0

    structuring_element = disk(5)

    binary_img = closing(binary_img, structuring_element)

    # bin_filtered = bwareafilt(binary_img, 2)

    possible_fish_num = 1

    if not is_empty_img(bin_filtered):
        fish = which_object_is_fish()



    else:
        input_img.fish_props.is_fish = False

    return input_img


def which_object_is_fish(binary_img: np.ndarray, mask: Mask, input_img: InputImage):
    height, width = input_img.size()

    bigger_binary_img = binary_img
    labels, label_numbers = scipy.ndimage.label(binary_img)

    temp_fish_bools = np.zeros(label_numbers)

    for i in range(label_numbers):
        obj = get_objects(i, labels)

        obj_cc = obj.cc

        temp_fish, fish_props = is_fish(labels)

        if temp_fish:
            pass
    ## TODO: itt maradt abba
    return


def check_fishy_props_fst(possible_fish, mask, input_img: InputImage):
    structuring_element = morphology.disk(51)
    complement_img = (~possible_fish)

    filled_img = (~(morphology.opening(complement_img, structuring_element)))

    complement_mask = ~mask
    complement_bigger_circle = modify_circle(complement_mask, 5, 'd')

    return


def more_fisher_object(first_possible_fish, second_possible_fish):
    return
