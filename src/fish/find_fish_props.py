import cv2
import numpy as np
from PIL import ImageFilter, Image
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist, rescale_intensity
from skimage.morphology import area_opening, binary_closing, disk

from src.filters import normalize_0_255
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
    binary_img = adaptiveTh(norm, block_size=7)  # adaptive thresholding

    # Get possible fish
    binary_img = area_opening(binary_img, 100).astype(float)  # area_opening
    binary_img = binary_closing(binary_img, disk(3)).astype(float)  # area_opening

    msg("Removing meniscus")
    meniscus = get_meniscus_effect(binary_img, input_img.well_props.mask.cropped).astype(float)
    binary_img = binary_img - meniscus
    input_img.processed = keep_largest_object(binary_img, filled=True)

    image = Image.fromarray(input_img.processed)
    image = image.filter(ImageFilter.ModeFilter(size=13))
    input_img.processed = image.__array__()

    show_img(input_img.processed)
    return input_img
