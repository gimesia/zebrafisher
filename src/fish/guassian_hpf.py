import numpy as np
from skimage.morphology import dilation, erosion, square
from skimage.exposure import equalize_hist
import cv2 as cv

from src.models import InputImage


def gaussian_high_pass_filter(input_img: InputImage):
    input_img.processed = gaussian_hpf(input_img.processed, input_img.well_props.mask.cropped)
    return input_img


def gaussian_hpf(img: np.ndarray, mask: np.ndarray):
    hpf = img - cv.GaussianBlur(img, (21, 21), 3) + 100
    equalized = equalize_hist(hpf)
    return np.multiply(equalized, mask)
