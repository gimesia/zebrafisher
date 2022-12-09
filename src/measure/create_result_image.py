import os

import cv2
import numpy as np
from skimage.color import gray2rgb
from skimage.io import imsave

from ..models import InputImage
from ..utils import show_img


def save_result_image(input_img: InputImage, popups=False):
    """
    Saves the result image into the output folder

    :param input_img: InputImage object with filled properties
    """
    res = create_result_image(input_img)
    if popups:
        show_img(res, f"{input_img.name}: Segmented")

    cwd = os.getcwd()
    path = os.path.join(cwd, "images", "out")
    # print(f"Saving image to {path}")
    os.chdir(path)
    if dir == "":
        filename = f"{input_img.name}_processed.jpg"
    else:
        filename = f"{input_img.name}_processed.jpg"

    filename = filename.replace("\\", "__")
    print(f'{filename}')

    cv2.imwrite(filename, res)
    os.chdir(cwd)


def create_result_image(input_img: InputImage) -> np.ndarray:
    """
    Creates image where the segmented areas are outlined with different colors

    :return: RGB image of the original with the marked lines
    """
    bbox_well = input_img.well_props.bounding_box
    bbox_fish = input_img.fish_props.bounding_box_well

    cropped_w = gray2rgb(input_img.og)
    cropped_f = bbox_fish.bound_img(bbox_well.bound_img(cropped_w))

    eye_contours = input_img.fish_props.eyes.astype(np.uint8)
    fish_contours = input_img.fish_props.mask.cropped.astype(np.uint8)

    eye_contours, h = cv2.findContours(eye_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fish_contours, h = cv2.findContours(fish_contours, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_NONE)

    cv2.circle(cropped_w, input_img.well_props.center, input_img.well_props.radius, (0, 0, 255),2)
    cv2.drawContours(cropped_f, fish_contours, -1, (0, 255, 0), 2)
    cv2.drawContours(cropped_f, eye_contours, -1, (255, 0, 0), 2)

    cropped_w = bbox_well.bound_img(cropped_w)
    cropped_w[bbox_fish.x1:bbox_fish.x2, bbox_fish.y1:bbox_fish.y2] = cropped_f

    res = gray2rgb(input_img.og)
    res[bbox_well.x1:bbox_well.x2, bbox_well.y1:bbox_well.y2] = cropped_w
    return res
