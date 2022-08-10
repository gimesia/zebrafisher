import numpy as np
from skimage.measure import regionprops_table, label
from skimage.morphology import remove_small_objects


def keep_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one
    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(binary_img.astype(int), properties=('area', 'label'))
    max_area = props['area'].max()
    removed = remove_small_objects(binary_img.astype(bool), max_area - (max_area * 0.2)).astype(np.uint8)
    return removed


"""def get_objects(label_num: int, labels) -> object:
    \"""
Actually
IDK
yet
what
this
does

:param: label_num
:param: labels
:rtype: object
\"""
cc = np.isin(labels, label_num)
(r, c) = np.where(cc > 0)

obj: object
obj.cc = cc
obj.shape = (r, c)

return obj
"""
