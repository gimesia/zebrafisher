import cv2
import numpy as np
from skimage.exposure import equalize_adapthist
from skimage.filters.edges import sobel
from skimage.morphology import area_opening

from src.filters import normalize_0_255
from src.models import InputImage
from src.utils.terminal_msg import show_img, msg


def edge_finding(img: np.ndarray, mask=None) -> np.ndarray:  # Function replacing edge filter
    edges = sobel(img, mask)  # range-filter
    edges = equalize_adapthist(edges)
    return normalize_0_255(edges)  # stretch contrast


def denoising(img: np.ndarray, strength=20) -> np.ndarray:
    return cv2.fastNlMeansDenoising(img, None, strength)  # denoise
    # return wiener(img, (30,30))


def adaptiveTh(img: np.ndarray, block_size=7) -> np.ndarray:
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 1)


def area_open(img: np.ndarray, th=500):
    return area_opening(img, area_threshold=th)


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    input_img.processed = edge_finding(input_img.processed, input_img.well_props.mask.cropped)  # rangefilter

    input_img.processed = denoising(input_img.processed)  # denoise

    input_img.processed = adaptiveTh(input_img.processed, block_size=3)  # adaptive thresholding

    # Get possible fish
    input_img.processed = area_open(input_img.processed, 100).astype(bool)  # area_opening

    return input_img
