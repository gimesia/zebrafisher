import numpy as np
from skimage.morphology import disk, dilation, erosion, area_opening

from src.models.InputImage import InputImage


def get_meniscus_for_input_img(input_img: InputImage, corrected=False) -> np.ndarray:
    binary_img = input_img.binary
    well_mask = input_img.well_props.mask.cropped

    return get_meniscus(binary_img, well_mask)


def get_meniscus(binary_img: np.ndarray, mask: np.ndarray, corrected=False) -> np.ndarray:
    if binary_img.shape != mask.shape:
        raise Exception("Arguments 'binary_img' and 'well_mask' must have equal shape" +
                        f"\n'binary_img': {binary_img.shape} != 'well_mask': {mask.shape}")

    possible_well_size_th = np.zeros_like(binary_img)
    remaining_binary_img = binary_img

    if not corrected:
        structuring_element = disk(21)
        eroded_well = erosion(mask, structuring_element)
        remaining_binary_img[np.where(eroded_well > 0)] = 0
    #    remaining_binary_img = morphology.area_opening(remaining_binary_img, 100)

    mh, mw = binary_img.shape
    h_center, w_center = int(mh / 2), int(mw / 2)

    lt = remaining_binary_img[0:h_center, 0:w_center]
    lb = remaining_binary_img[h_center:mh, 0:w_center]
    rt = remaining_binary_img[0:h_center, w_center:mw]
    rb = remaining_binary_img[h_center:mh, w_center:mw]

    """lt_thresh = get_mean_col_sum_for_structuring_element(lt, "lt", corrected)
    lb_thresh = get_mean_col_sum_for_structuring_element(lb, "lb", corrected)
    rt_thresh = get_mean_col_sum_for_structuring_element(rt, "rt", corrected)
    rb_thresh = get_mean_col_sum_for_structuring_element(rb, "rb", corrected)"""

    left_side = np.concatenate((lt, lb), axis=0)
    right_side = np.concatenate((rt, rb), axis=0)
    full = np.concatenate((left_side, right_side), axis=1)

    return full


def get_mean_col_sum_for_structuring_element(data: np.ndarray, corner: str,
                                             corrected_step: bool = False):  # cont, mod_cont
    thresh_well = np.zeros_like(data.shape)

    col_sum = np.sum(data[-1:1])  # in matlab ->   data'
    mean_data = np.floor(np.mean(col_sum[(col_sum > 0)]))
    """
        if not corrected_step:
            img = cont
        else:
            img = mod_cont
    """
    if not np.isnan(mean_data):
        structuring_element = disk(mean_data)
        if corner == 'lt':
            thresh_well = dilation(
                data[0:np.floor(data.shape[0] / 2), 0:np.floor(data.shape[1] / 2)],
                structuring_element)
        elif corner == 'lb':
            thresh_well = dilation(
                data[np.floor(data.shape[0] / 2):data.shape[0], 0:np.floor(data.shape[1] / 2)],
                structuring_element)
        elif corner == 'rt':
            thresh_well = dilation(
                data[0:np.floor(data.shape[0] / 2), np.floor(data.shape[1] / 2):data.shape[1]],
                structuring_element)
        elif corner == 'rb':
            thresh_well = dilation(
                data[np.floor(data.shape[0] / 2):data.shape[0],
                np.floor(data.shape[1] / 2):data.shape[1]],
                structuring_element)

    return thresh_well
