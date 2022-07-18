import math
import numpy as np

from src.InputImage import InputImage
from src.terminal_msg import msg


def triangle_threshold(input_img: InputImage) -> float:
    msg("Calculating triangle threshold")

    [histogram, bins] = np.histogram(input_img.processed, bins=255)

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
        histogram = histogram.reshape(1, -1)
        histogram = np.fliplr(np.transpose(histogram))
        # histogram = np.fliplr(histogram)
        a = bins_count - last_non_zero  # No need for the +1, because IDK
        b = bins_count - max_index  # No need for the +1, because IDK
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

    # Obtain threshold as the location of maximum distance
    # level = (np.max(distances) == distances).nonzero()

    # TODO!! EZT MÉG MEG KELL CSINÁLNI JÓRA ÉS KÉSZE EZ A MODUL!
    level = (np.max(distances) == distances)
    level = np.argwhere(level == True)
    import matplotlib.pyplot as plt
    plt.plot(histogram)
    plt.show()


"""    try:
        max_index = math.floor(np.mean(max_index))
    finally:
        pass"""

if __name__ == '__main__':
    img = InputImage("zf.png")
    triangle_threshold(img)
