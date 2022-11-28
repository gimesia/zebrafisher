import cv2
import numpy as np
from skimage.measure import find_contours

from src.models import InputImage


def create_result_image(input_img: InputImage) -> np.ndarray:
    res = np.zeros_like(input_img.og)
    bbox_well = input_img.well_props.bounding_box
    bbox_fish = input_img.fish_props.bounding_box_well

    eye_contours = find_contours(input_img.fish_props.eyes)
    fish_contours = find_contours(input_img.fish_props.mask.cropped)
    well_contours = find_contours(input_img.well_props.mask.og)

    print(eye_contours)
    print(fish_contours)
    print(well_contours)

    return res