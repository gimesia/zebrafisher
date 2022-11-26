from typing import Tuple

import numpy as np
from skimage.exposure import adjust_gamma, equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion, disk, binary_opening, binary_dilation, binary_closing

from src.models import BoundingBox, InputImage
from .get_head import should_be_rotated, get_head, get_two_sides_img, get_two_sides_bbox
from ..utils import show_img, msg, keep_2_largest_object


def get_eyes(input_img: InputImage) -> InputImage:
    """
    Segments potential eye region(s) from convex mask of fish

    :param input_img: InputImage object the convex fish mask calculated

    :rtype: InputImage object with filled 'fish_props.eyes' property
    """
    mask = input_img.fish_props.mask.og
    cropped_mask = input_img.fish_props.mask.cropped
    masked = adjust_gamma((unsharp_mask(input_img.fish_props.cropped_og, radius=2) * mask), gamma=2)

    # Rotating if width < height
    if should_be_rotated(input_img.fish_props.mask.cropped):
        masked = np.transpose(masked)
        mask = np.transpose(mask)
        input_img.fish_props.rotated = True

    # Splitting images and masks in half
    sides = get_two_sides_img(masked)  # masked
    sides_mask = get_two_sides_img(mask)
    sides_cropped_mask = get_two_sides_img(cropped_mask)

    # Calculating head region
    msg("Getting head of fish")
    head, side = get_head(input_img.fish_props.mask.cropped)
    if side == "l":
        input_img.fish_props.head = "l"
        head = sides[0]
        head_mask = sides_mask[0]
        head_cropped_mask = sides_cropped_mask[0]
    elif side == "r":
        input_img.fish_props.head = "r"
        head = sides[1]
        head_mask = sides_mask[1]
        head_cropped_mask = sides_cropped_mask[1]
    else:
        raise Exception("Invalid head side!")

    head = equalize_adapthist(head)  # Expanding distance between bins

    mean = np.mean(head[head_mask != 0])  # Mean intensity of image

    th = (head < mean * 0.3) * head_mask  # thresholding

    th = eye_spy(th)  # filtering out possible eye objects
    th = remove_hind_objects(th, side)  # removing objects in the hindsight of the head part

    are_eyes, eye_count = check_eyes(th)

    if eye_count > 2:
        if eye_count > 5:
            msg(f"Found more than 5 possible eyes found: {eye_count}")
            input_img.fish_props.has_eyes = False
            input_img.fish_props.eyes = np.zeros_like(head)
            return input_img
        if 5 >= eye_count:  # If there are only a few objects present, we only keep the 2 largest
            msg(f"Found more than 2 possible eyes found: {eye_count} -> keeping the 2 largest")
            th = keep_2_largest_object(th)
            are_eyes, eye_count = check_eyes(th)

    if eye_count == 1:
        msg("Only found one eye!")
        input_img.fish_props.has_eyes = True
    elif eye_count == 2:
        msg("Found 2 eyes!")
        input_img.fish_props.has_eyes = True
    elif eye_count == 0:
        msg("No eyes found!")
        input_img.fish_props.eyes = np.zeros_like(head)
        input_img.fish_props.has_eyes = False
        return input_img  # Returns if there were no eyes found

    th = binary_dilation(th, disk(3))  # Dilating previously eroded objects

    input_img.fish_props.eyes = th

    # Adding eyes to the cropped mask
    head_with_eyes = np.logical_or(th, head_cropped_mask)
    if side == "l":
        cropped_mask = np.concatenate([head_with_eyes, sides_cropped_mask[1]], axis=1)
    elif side == "r":
        cropped_mask = np.concatenate([sides_cropped_mask[0], head_with_eyes], axis=1)

    cropped_mask = binary_closing(cropped_mask, disk(15))  # Closing any fitting imperfections
    input_img.fish_props.mask.cropped = cropped_mask

    """
    THIS ROTATES THE FISH AND THE MASKS BACK TO THEIR ORIGINAL ORIENTATION
    if input_img.fish_props.rotated:
        input_img.fish_props.mask.og = input_img.fish_props.mask.og.transpose()
        input_img.fish_props.mask.cropped = input_img.fish_props.mask.cropped.transpose()
        input_img.fish_props.cropped_og = input_img.fish_props.cropped_og.transpose()"""

    return input_img


def eye_spy(fish: np.ndarray):
    msg("Searching for eye regions")
    fish = binary_erosion(fish, disk(3))
    fish = binary_opening(fish, disk(3))
    props = regionprops(label(fish))
    props = list(filter(eye_criteria, props))

    rem = put_rprops_on_empty(fish.shape, props)
    return rem


def eye_criteria(x) -> bool:
    if x.eccentricity > 0.92:
        return False
    if x.area < 300 or x.area > 2000:
        return False
    if x.solidity < 0.5:
        return False
    return True


def remove_hind_objects(bin_img: np.ndarray, side: str) -> np.ndarray:
    """
    Keeps objects only on one side (left,right) of the image

    :param bin_img: input binary image
    :param side: 'l' for left, 'r' for right
    :return: input image containing object on one side
    """
    msg("Removing objects close to the middle of the embryo")
    cw = int(bin_img.shape[1] / 2)
    props = regionprops(label(bin_img))
    if side == 'l':
        props = list(filter(lambda x: x.bbox[1] < cw, props))
    if side == 'r':
        props = list(filter(lambda x: x.bbox[1] > cw, props))
    return put_rprops_on_empty(bin_img.shape, props)


def check_eyes(bin_img: np.ndarray) -> (bool, int):
    props = regionprops(label(bin_img))
    return True if 3 > len(props) > 0 else False, len(props)


def put_rprops_on_empty(shape: (int, int), rprops, convex: bool = False):
    rem = np.zeros(shape)
    for i_, r in enumerate(rprops):
        bbox = BoundingBox()
        bbox.set(r.bbox)
        if not convex:
            rem[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = r.image_filled
        else:
            rem[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = r.image_convex
    return rem
