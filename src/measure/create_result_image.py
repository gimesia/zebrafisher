import cv2
import numpy as np
from skimage.color import gray2rgb
from skimage.measure import find_contours

from src.models import InputImage
from src.utils import show_img


def create_result_image(input_img: InputImage) -> np.ndarray:
    bbox_well = input_img.well_props.bounding_box
    bbox_fish = input_img.fish_props.bounding_box_well

    cropped_w = gray2rgb(input_img.og)
    cropped_f = bbox_fish.bound_img(bbox_well.bound_img(cropped_w))

    eye_contours = input_img.fish_props.eyes.astype(np.uint8)
    fish_contours = input_img.fish_props.mask.cropped.astype(np.uint8)

    eye_contours, hierarchy = cv2.findContours(eye_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fish_contours, hierarchy = cv2.findContours(fish_contours, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)

    cv2.circle(cropped_w, input_img.well_props.center, input_img.well_props.radius, (0, 0, 255))
    cv2.drawContours(cropped_f, fish_contours, -1, (0, 255, 0), 2)
    cv2.drawContours(cropped_f, eye_contours, -1, (255, 0, 0), 2)

    # show_img(cropped_w)
    # show_img(cropped_f)

    cropped_w = bbox_well.bound_img(cropped_w)
    cropped_w[bbox_fish.x1:bbox_fish.x2, bbox_fish.y1:bbox_fish.y2] = cropped_f
    res = gray2rgb(input_img.og)
    res[bbox_well.x1:bbox_well.x2, bbox_well.y1:bbox_well.y2] = cropped_w
    return res
