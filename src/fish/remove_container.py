import numpy as np
from skimage.morphology import disk, erosion, binary_dilation, square


def get_perimeter(bin_img: np.ndarray) -> np.ndarray:
    """

    @rtype: mask of perimeter
    """
    bw = bin_img
    se = disk(5)
    bw_erode = erosion(bw, se)
    return np.abs(np.subtract(bw_erode, bw))


def get_meniscus_effect(binary_img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Contracts the meniscus effect calculated from the mask's perimeter

    @rtype: binary image of the container
    """
    remaining_binary_img = binary_img.copy()

    mh, mw = binary_img.shape[0], binary_img.shape[1]
    ch, cw = int(mh / 2), int(mw / 2)

    lt = remaining_binary_img[0:ch, 0:cw]
    lb = remaining_binary_img[ch:mh, 0:cw]
    rt = remaining_binary_img[0:ch, cw:mw]
    rb = remaining_binary_img[ch:mh, cw:mw]

    cont = get_perimeter(mask).astype(bool)
    lt_c = cont[0:ch, 0:cw]
    lb_c = cont[ch:mh, 0:cw]
    rt_c = cont[0:ch, cw:mw]
    rb_c = cont[ch:mh, cw:mw]

    lt_thresh = rc(lt, lt_c, 3)
    lb_thresh = rc(lb, lb_c, 3)
    rt_thresh = rc(rt, rt_c, 3)
    rb_thresh = rc(rb, rb_c, 3)

    # plot_images([lt_thresh, rt_thresh, lb_thresh, rb_thresh], 2)

    left_side = np.concatenate((lt_thresh, lb_thresh), axis=0)
    right_side = np.concatenate((rt_thresh, rb_thresh), axis=0)
    full = np.concatenate((left_side, right_side), axis=1)

    return full


def rc(data: np.ndarray, cont: np.ndarray, se: int) -> np.ndarray:
    """
    Recursive function that dilates the container until it has less than 45% True values, when masked with the original

    @rtype: the dilated container
    """
    cont = binary_dilation(cont, square(se))
    dilated_cont_masked = data * cont

    perimeter_nonzero = len(cont.nonzero()[0])
    masked_nonzero = len(dilated_cont_masked.nonzero()[0])
    if perimeter_nonzero == 0:
        return data

    filled = masked_nonzero / perimeter_nonzero
    if filled > 0.45:
        return rc(data, cont, se + 1)
    return dilated_cont_masked
