import numpy as np
from skimage.morphology import dilation, erosion, square
from skimage.exposure import equalize_hist
import cv2 as cv

from src.models import InputImage
from src.terminal_msg import msg


def gaussian_high_pass_filter(input_img: InputImage):
    msg("Applying Gaussian HPF to enhance edges of the embryo")
    input_img.processed = gaussian_hpf(input_img.processed, input_img.well_props.mask.cropped)
    return input_img


def gaussian_hpf(img: np.ndarray, mask: np.ndarray):
    hpf = img - cv.GaussianBlur(img, (21, 21), 3) + 100  # Applying filter
    equalized = equalize_hist(hpf)  # Equalizing values for better separation
    return np.multiply(equalized, mask)
