import numpy as np


def get_objects(label_num: int, labels) -> object:
    """
    Actually IDK yet what this does

    :param: label_num
    :param: labels
    :rtype: object
    """
    cc = np.isin(labels, label_num)
    (r, c) = np.where(cc > 0)

    obj: object
    obj.cc = cc
    obj.shape = (r, c)

    return obj
