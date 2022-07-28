import numpy as np
from skimage.morphology import disk, dilation, erosion, area_opening

from src import Mask


def get_plate_width_and_remove_sides(binary_img: np.ndarray, well_mask: Mask, corrected=False):
    possible_well_size_th = np.zeros_like(binary_img)

    remaining_binary_img = binary_img

    if not corrected:
        structuring_element = disk(21)
        eroded_well = erosion(well_mask.cropped)

        remaining_binary_img[np.where(eroded_well > 0)] = 0
        remaining_binary_img = area_opening(remaining_binary_img, 100)

    [mh, mw] = binary_img.shape

    return


def get_mean_col_sum_for_structuring_element(data: np.ndarray, corner: str, corrected_step: bool, cont, mod_cont):
    thresh_well = np.zeros_like(data.shape)

    col_sum = np.sum(data[-1:1])  # in matlab ->   data'
    mean_data = np.floor(np.mean(col_sum > 0))

    if not corrected_step:
        img = cont
    else:
        img = mod_cont

    if not np.isnan(mean_data):
        structuring_element = disk(mean_data)
        if corner == 'lt':
            thresh_well = dilation(
                img[0:np.floor(img.shape[0] / 2), 0:np.floor(img.shape[1] / 2)],
                structuring_element)
        elif corner == 'lb':
            thresh_well = dilation(
                img[np.floor(img.shape[0] / 2):img.shape[0], 0:np.floor(img.shape[1] / 2)], structuring_element)
        elif corner == 'rt':
            thresh_well = dilation(
                img[0:np.floor(img.shape[0] / 2), np.floor(img.shape[1] / 2):img.shape[1]], structuring_element)
        elif corner == 'rb':
            thresh_well = dilation(
                img[np.floor(img.shape[0] / 2):img.shape[0], np.floor(img.shape[1] / 2):img.shape[1]],
                structuring_element)

    return thresh_well
