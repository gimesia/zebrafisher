import cv2
import numpy as np
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import binary_closing, disk, binary_dilation

from src.filters import normalize_0_255, yen_th, normalize_0_1
from src.models import InputImage, BoundingBox
from src.utils.terminal_msg import msg, show_img
from .rangefilter import range_filter
from .remove_container import get_meniscus_effect
from ..utils import keep_largest_object, keep_largest_object_convex, get_bounding_box_obj, bbox_addition


def adaptiveTh(img: np.ndarray, block_size=7) -> np.ndarray:
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 1)


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    msg("Applying range-filter")
    eq = unsharp_mask(input_img.processed, radius=2)  # sharpening
    rngfilter = range_filter(eq, input_img.well_props.mask.cropped)  # rangefilter
    normalized = normalize_0_1(rngfilter)
    normalized = equalize_adapthist(normalized)

    msg("Applying wiener-filter")
    input_img.processed = wiener(normalized, mysize=30)  # denoising with wiener filter
    norm = normalize_0_255(input_img.processed)

    msg("Applying adaptive-threshold")
    binary_img = yen_th(norm)  # adaptiveTh(norm, block_size=7)  # adaptive thresholding
    # show_img(binary_img, 'th')

    # Get possible fish
    binary_img = binary_closing(binary_img, disk(3))
    # show_img(binary_img, 'closing')

    msg("Removing meniscus")
    meniscus = get_meniscus_effect(binary_img, input_img.well_props.mask.cropped).astype(float)
    binary_img = binary_img - meniscus
    # show_img(binary_img, 'menisc')

    msg("Keeping only the possible fish")
    binary_img = keep_largest_object(binary_img, filled=True).astype(bool)
    # show_img(binary_img, 'klo')




    convex_mask = keep_largest_object_convex(binary_img)
    convex_mask = binary_dilation(convex_mask, disk(10))

    convex = convex_mask * input_img.well_props.mask.cropped_masked
    # show_img(convex, 'convex')

    bbox_ = get_bounding_box_obj(convex_mask)
    """    im = input_img.well_props.mask.cropped_masked
    im[bbox_.x1:bbox_.x2, bbox_.y1:bbox_.y2] = 255"""

    bbox = BoundingBox(input_img.well_props.bounding_box.x1 + bbox_.x1,
                       input_img.well_props.bounding_box.y1 + bbox_.y1,
                       input_img.well_props.bounding_box.x1 + bbox_.x2,
                       input_img.well_props.bounding_box.y1 + bbox_.y2)
    """
    im_ = input_img.well_props.mask.masked
    im_[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = 255
    show_img(im_, 'im')
    """

    input_img.fish_props.bounding_box = bbox
    input_img.fish_props.mask.cropped_masked = input_img.og[bbox.x1:bbox.x2, bbox.y1:bbox.y2]

    th = yen_th(input_img.fish_props.mask.cropped_masked)

    input_img.processed = binary_img
    return input_img


def refine_mask():
    pass
