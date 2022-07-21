import numpy as np

from src.InputImage import EXAMPLE_IMG
from src.filters.high_boost_filter import high_boost_filter
from src.filters.normalize_intensity_range import normalize_0_1, normalize_min_max
from src.terminal_msg import show_img
from src.well.find_well_props import find_well_props

"""Note: I removed the 'varargin' parameter in og MATLAB code, because I think I will have no other use for it"""


def homomorphic(img: np.ndarray, cut_off, order, boost):
    # img = normalize_0_1(img)  # Rescale values 0-1 (and cast to `double' if needed).

    fft_log_img: np.ndarray = np.fft.fft2(np.log(img + 0.01))  # Take FFT of log (with offset to avoid log of 0).

    hbf = high_boost_filter(img.shape, cut_off, order, boost)  # Apply the filter, invert fft, and invert the log.

    if fft_log_img.shape[1] > hbf.shape[1]:
        fft_log_img = fft_log_img[:, :-1]

    if fft_log_img.shape[0] > hbf.shape[0]:
        fft_log_img = fft_log_img[:-1, :]

    hmf = np.exp(np.real(np.fft.ifft2(fft_log_img * hbf)))

    return normalize_0_1(hmf)


if __name__ == "__main__":
    img = find_well_props(EXAMPLE_IMG).processed
    img = homomorphic(img, 0.015, 2, 1.5)
    img = normalize_min_max(img, (0, 255))
    show_img(img)
