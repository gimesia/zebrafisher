import numpy as np
from skimage.morphology import disk, dilation, erosion, area_opening

from src.models.InputImage import InputImage


def get_perimeter(bin_img: np.ndarray) -> np.ndarray:
    bw = bin_img
    se = disk(5)
    bw_erode = erosion(bw, se)
    return np.abs(np.subtract(bw_erode, bw))


def get_meniscus(binary_img: np.ndarray, mask: np.ndarray, corrected=False) -> np.ndarray:
    remaining_binary_img = binary_img.copy()

    if not corrected:
        structuring_element = disk(21)
        eroded_well = erosion(mask, structuring_element)
        remaining_binary_img[np.where(eroded_well > 0)] = 0
        remaining_binary_img = area_opening(remaining_binary_img, area_threshold=100).astype(bool)

    mh, mw = binary_img.shape[0], binary_img.shape[1],
    ch, cw = int(mh / 2), int(mw / 2)

    lt = remaining_binary_img[0:ch, 0:cw]
    lb = remaining_binary_img[ch:mh, 0:cw]
    rt = remaining_binary_img[0:ch, cw:mw]
    rb = remaining_binary_img[ch:mh, cw:mw]

    cont = get_perimeter(mask)

    lt_thresh = mean_4_col_sum(lt, "lt", cont)
    lb_thresh = mean_4_col_sum(lb, "lb", cont)
    rt_thresh = mean_4_col_sum(rt, "rt", cont)
    rb_thresh = mean_4_col_sum(rb, "rb", cont)

    left_side = np.concatenate((lt_thresh, lb_thresh), axis=0)
    right_side = np.concatenate((rt_thresh, rb_thresh), axis=0)
    full = np.concatenate((left_side, right_side), axis=1)

    return full


def mean_4_col_sum(data: np.ndarray, corner: str, cont: np.ndarray):
    thresh_well = np.zeros_like(data)

    col_sum = np.sum(data, axis=0)

    csum = col_sum[col_sum > 0]  # columns where sum > 0

    if len(csum) == 0: return data

    mean_data = (np.floor(np.mean(csum)))

    if not np.isnan(mean_data):
        se = disk(mean_data)

        mh, mw = cont.shape[0], cont.shape[1],
        ch, cw = int(mh / 2), int(mw / 2)

        if corner == 'lt':
            thresh_well = dilation(cont[0:ch, 0:cw], se)
        elif corner == 'lb':
            thresh_well = dilation(cont[ch:mh, 0:cw], se)
        elif corner == 'rt':
            thresh_well = dilation(cont[0:ch, cw:mw], se)
        elif corner == 'rb':
            thresh_well = dilation(cont[ch:mh, cw:mw], se)
    return thresh_well
