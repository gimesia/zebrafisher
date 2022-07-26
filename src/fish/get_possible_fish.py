import numpy as np
import scipy
from skimage import measure, filters, morphology

from src.InputImage import InputImage, Mask

cont = None
mod_cont = None


def get_possible_fish(input_img: InputImage):
    global cont
    global mod_cont

    segmented_fish_size_first = np.zeros_like(input_img.og)
    segmented_fish_size_second = np.zeros_like(input_img.og)

    # What is this name
    cont = measure.perimeter(input_img.well_props.mask.cropped)

    binary_img = morphology.area_opening(input_img.processed, 100)

    return input_img


def get_plate_width_and_remove_sides(binary_img: np.ndarray, well_mask: Mask, corrected=False):
    possible_well_size_th = np.zeros_like(binary_img)

    remaining_binary_img = binary_img

    if not corrected:
        structuring_element = morphology.disk(21)
        eroded_well = morphology.erosion(well_mask.cropped)

        remaining_binary_img[np.where(eroded_well > 0)] = 0
        remaining_binary_img = morphology.area_opening(remaining_binary_img, 100)

    [mh, mw] = binary_img.shape

    return


def get_mean_col_sum_for_structuring_element(data: np.ndarray, corner: str, corrected_step: bool):
    global cont
    global mod_cont

    thresh_well = np.zeros_like(data.shape)

    col_sum = np.sum(data)  # in matlab ->   data'
    mean_data = np.floor(np.mean(col_sum(col_sum > 0)))

    if not corrected_step:
        img = cont
    else:
        img = mod_cont

    if not np.isnan(mean_data):
        structuring_element = morphology.disk(mean_data)
        if corner == 'lt':
            thresh_well = morphology.dilation(
                img[0:np.floor(img.shape[0] / 2), 0:np.floor(img.shape[1] / 2)],
                structuring_element)
        elif corner == 'lb':
            thresh_well = morphology.dilation(
                img[np.floor(img.shape[0] / 2):img.shape[0], 0:np.floor(img.shape[1] / 2)], structuring_element)
        elif corner == 'rt':
            thresh_well = morphology.dilation(
                img[0:np.floor(img.shape[0] / 2), np.floor(img.shape[1] / 2):img.shape[1]], structuring_element)
        elif corner == 'rb':
            thresh_well = morphology.dilation(
                img[np.floor(img.shape[0] / 2):img.shape[0], np.floor(img.shape[1] / 2):img.shape[1]],
                structuring_element)

    return thresh_well


def is_fish(labeled_data: np.ndarray) -> [bool, object]:
    reg_props = measure.regionprops(labeled_data)

    if reg_props[0].eccentricity < 0.9:  # 0.92
        fish = True
    else:
        fish = False

    props: object

    props.area = reg_props[0].area
    props.obj_height = reg_props[0].bbox[3] - reg_props[0].bbox[1]  # y2-y1
    props.obj_width = reg_props[0].bbox[2] - reg_props[0].bbox[0]  # x2-x1

    return fish, props


def get_objects(label_num: int, labels) -> object:
    cc = np.isin(labels, label_num)
    (r, c) = np.where(cc > 0)

    obj: object
    obj.cc = cc
    obj.shape = (r, c)

    return obj


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
    ## TODO: itt maradt abba
    return


def check_fishy_props_fst(possible_fish, mask, input_img: InputImage):
    structuring_element = morphology.disk(51)
    complement_img = (~possible_fish)

    filled_img = (~(morphology.opening(complement_img, structuring_element)))

    complement_mask = ~mask
    complement_bigger_circle = modify_circle(complement_mask, 5, 'd')

    return


def modify_circle(img: np.ndarray, kernel_size: int, e_or_d):
    structuring_element = morphology.disk(kernel_size)
    if e_or_d == "e":
        return morphology.erosion(img, structuring_element)
    elif e_or_d == "d":
        return morphology.dilation(img, structuring_element)
    else:
        raise Exception('put \'e\' or \'d\' as 3rd param')

def more_fisher_object(first_possible_fish, second_possible_fish):
