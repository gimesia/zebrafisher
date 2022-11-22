import numpy as np
from skimage.exposure import adjust_gamma, equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects, binary_erosion, disk, binary_dilation, binary_opening, \
    binary_closing

from .get_head import should_be_rotated, get_head, get_two_sides_img
from src.models import BoundingBox, InputImage
from ..utils import show_img


def eye_criteria(x):
    # if x.eccentricity > 0.92: return False
    if x.area < 250:
        return False
    if x.solidity < 0.55:
        return False
    return True


def eye_spy(fish: np.ndarray):
    rem = np.zeros_like(fish)

    fish = binary_erosion(fish, disk(3))
    fish = binary_opening(fish, disk(3))
    labeled = label(fish)
    rp = regionprops(labeled)

    rp = list(filter(eye_criteria, rp))

    for i_, r in enumerate(rp):
        bbox = BoundingBox()
        bbox.set(r.bbox)
        rem[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = r.image_convex
    return rem


def get_eyes(input_img: InputImage) -> InputImage:
    mask = input_img.fish_props.mask.og
    masked = adjust_gamma((unsharp_mask(input_img.fish_props.cropped_og, radius=2) * mask), gamma=2)

    if should_be_rotated(input_img.fish_props.mask.cropped):
        masked = np.transpose(masked)
        mask = np.transpose(mask)
        input_img.fish_props.rotated = True

    sides = get_two_sides_img(masked)  # masked)
    sides_mask = get_two_sides_img(mask)

    # head, side = get_head(masked)
    head, side = get_head(input_img.fish_props.mask.cropped)
    if side == 'l':
        head = sides[0]
        head_mask = sides_mask[0]
    else:
        head = sides[1]
        head_mask = sides_mask[1]

    head = equalize_adapthist(head)

    i = np.where(head_mask.astype(bool) == True)

    mean = np.mean(head[i])

    th = (head < mean * 0.35) * head_mask  # thresholding
    show_img(th)
    th = eye_spy(th)  # filtering out possible eye objects

    input_img.processed = th
    input_img.fish_props.eyes = th
    if input_img.fish_props.rotated:
        input_img.fish_props.mask.og = input_img.fish_props.mask.og.transpose()
        input_img.fish_props.mask.cropped = input_img.fish_props.mask.cropped.transpose()
        input_img.fish_props.cropped_og = input_img.fish_props.cropped_og.transpose()

    return input_img
