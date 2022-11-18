import numpy as np
from skimage.morphology import disk, erosion, binary_dilation, square


def get_perimeter(bin_img: np.ndarray) -> np.ndarray:
    """
    Returns the perimeter line of a binary image

    @rtype: mask of perimeter
    """
    bw = bin_img
    se = disk(5)
    bw_erode = erosion(bw, se)
    return np.abs(np.subtract(bw_erode, bw))


def recursive_meniscus_analysis(data: np.ndarray, cont: np.ndarray, se: np.ndarray, i: int = 1) -> np.ndarray:
    """
    Recursive function that dilates the container until it has less than 45% True values, when masked with the original

    :rtype: np.ndarray
    :return: dilated container
    """
    cont = binary_dilation(cont, se)
    dilated_cont_masked = data * cont

    perimeter_nonzero = len(cont.nonzero()[0])
    masked_nonzero = len(dilated_cont_masked.nonzero()[0])

    if perimeter_nonzero == 0:
        return data, i

    filled = masked_nonzero / perimeter_nonzero

    if filled > 0.45:
        return recursive_meniscus_analysis(data, cont, se, i + 1)
    return cont, i


def iterative_dilation(img: np.ndarray, iterations: int, se: np.ndarray):
    for i in range(iterations):
        img = binary_dilation(img, se)
    return img


def get_meniscus_effect_(binary_img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Contracts the meniscus effect calculated from the mask's perimeter

    @rtype: binary image of the container
    """
    remaining_binary_img = binary_img.copy()

    lt, lb, rt, rb = divide_into_quarters(remaining_binary_img)

    perimeter = get_perimeter(mask).astype(bool)
    lt_c, lb_c, rt_c, rb_c = divide_into_quarters(perimeter)

    se = disk(3)
    lt_thresh, lt_iters = recursive_meniscus_analysis(lt, lt_c, se, 1)
    # print(f'{lt_iters}')
    lb_thresh, lb_iters = recursive_meniscus_analysis(lb, lb_c, se, 1)
    # print(f'{lb_iters}')
    rt_thresh, rt_iters = recursive_meniscus_analysis(rt, rt_c, se, 1)
    # print(f'{rt_iters}')
    rb_thresh, rb_iters = recursive_meniscus_analysis(rb, rb_c, se, 1)
    # print(f'{rb_iters}')

    mx = max([lt_iters, lb_iters, rt_iters, rb_iters])
    # print(f'max: {mx}')
    left_side = np.concatenate((iterative_dilation(lt_c, mx, se), iterative_dilation(lb_c, mx, se)), axis=0)
    right_side = np.concatenate((iterative_dilation(rt_c, mx, se), iterative_dilation(rb_c, mx, se)), axis=0)
    full = np.concatenate((left_side, right_side), axis=1)

    return full


def divide_into_quarters(img: np.ndarray) -> [np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Divides the image into 4 quarters

    :rtype: quarters of the image
    """
    mh, mw = img.shape[0], img.shape[1]
    ch, cw = int(np.round(mh / 2)), int(np.round(mw / 2))
    lt = img[0:ch, 0:cw]
    lb = img[ch:mh, 0:cw]
    rt = img[0:ch, cw:mw]
    rb = img[ch:mh, cw:mw]
    return [lt, lb, rt, rb]
