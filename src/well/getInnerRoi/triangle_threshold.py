# TODO! FIX LAST LINES!

import numpy as np

from src.InputImage import InputImage, PROTOTYPE_IMG
from src.terminal_msg import msg


def triangle_threshold(input_img: InputImage) -> float:
    msg("Calculating triangle threshold")

    [histogram, bins] = np.histogram(input_img.processed, bins=256)
    # np.savetxt('hist.csv', histogram, delimiter=",")
    bins_count = np.size(bins)

    # Find maximum of histogram and its location along the X axis
    max_value = np.amax(histogram)
    max_index = np.argmax(histogram)

    # Can have more than a single value!
    if isinstance(max_index, np.ndarray):
        max_index = np.around(np.mean(max_index))
        max_value = histogram[max_index]

    # Find location of first and last non-zero values. Values < h / 10000 are considered zeros.
    indexes = (histogram > max_value / 10000).nonzero()[0]
    first_non_zero = indexes[0]
    last_non_zero = indexes[-1]

    # Pick side as side with longer tail. Assume one tail is longer.
    left_span = max_index - first_non_zero
    right_span = last_non_zero - max_index

    if right_span > left_span:
        histogram = histogram.reshape(1, -1)  # Must do this because of fliplr
        histogram = np.fliplr(np.transpose(histogram))
        # histogram = np.fliplr(histogram)
        a = bins_count - last_non_zero - 1  # '-1' instead of the '+1' , in MATLAB because IDK
        b = bins_count - max_index - 1  # '-1' instead of the '+1' , in MATLAB because IDK
        is_flipped = True
    else:
        histogram = np.transpose(histogram)
        is_flipped = False
        a = first_non_zero
        b = max_index

    #  Compute parameters of the straight line from first non-zero to peak
    #  To simplify, shift X axis by a (bin number axis)
    m = max_value / (b - a)

    # Compute distances
    x_1 = np.arange(b - a + 1)
    y_1 = histogram[x_1 + a - 1]
    beta = y_1 + x_1 / m

    x_2 = beta / (m + 1 / m)
    y_2 = m * x_2

    distances = np.power((np.power((y_2 - y_1), 2) + np.power((x_2 - x_1), 2)), 0.5)

    # TODO!! EZT MÉG MEG KELL CSINÁLNI JÓRA ÉS KÉSZ EZ A MODUL!
    # Obtain threshold as the location of maximum distance
    max_index_list = list([])
    shp = distances.shape
    for i in range(shp[0]):
        max_value = np.max(distances[i])
        max_index = np.where(distances[i] == max_value)
        if len(max_index) > 1:
            for j in max_index:
                real_index_of_max = max_index[j][0] + (distances.shape[1] * i)
                max_index_list.append(real_index_of_max)

        real_index_of_max = max_index[0][0] + (distances.shape[1] * i)
        max_index_list.append(real_index_of_max)
    max_index_list = np.asarray(max_index_list)

    mean = np.mean(max_index_list)
    level = a + mean

    # Flip back if necessary
    if is_flipped:
        level = bins_count - level + 1
    # TODO! valami szar
    return level / bins_count


if __name__ == '__main__':
    img = PROTOTYPE_IMG
    res = triangle_threshold(img)
    print(res)

