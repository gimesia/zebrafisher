import cv2
import numpy as np
from PIL import ImageFilter, Image
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist, rescale_intensity
from skimage.morphology import area_opening, binary_closing, disk, binary_dilation, square

from src.filters import normalize_0_255, yen_th, iso_th
from src.models import InputImage
from src.utils.terminal_msg import msg, show_img
from .rangefilter import range_filter
from .remove_container import get_meniscus_effect
from ..utils import keep_largest_object


def adaptiveTh(img: np.ndarray, block_size=7) -> np.ndarray:
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 1)


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    msg("Applying range-filter")
    rngfilter = range_filter(input_img.processed, input_img.well_props.mask.cropped)  # rangefilter
    normalized = cv2.normalize(rngfilter, None, 0, 255, cv2.NORM_MINMAX)
    normalized = equalize_adapthist(normalized)

    msg("Applying wiener-filter")
    input_img.processed = wiener(normalized, mysize=30)  # denoising with wiener filter
    norm = normalize_0_255(input_img.processed)

    msg("Applying adaptive-threshold")
    binary_img = yen_th(norm)  # adaptiveTh(norm, block_size=7)  # adaptive thresholding
    show_img(binary_img, 'th')

    # Get possible fish
    binary_img = binary_closing(binary_img, disk(3))
    show_img(binary_img, 'closing')
    binary_img = area_opening(binary_img, 100).astype(bool)  # area_opening
    show_img(binary_img, 'opening')

    msg("Removing meniscus")
    meniscus = get_meniscus_effect(binary_img, input_img.well_props.mask.cropped).astype(float)
    binary_img = binary_img - meniscus
    show_img(binary_img, 'menisc')

    binary_img = keep_largest_object(binary_img, filled=True)

    input_img.processed = binary_img
    show_img(binary_img)
    a = binary_dilation(binary_img, square(10))
    show_img(binary_img * input_img.well_props.mask.cropped_masked)
    return input_img
