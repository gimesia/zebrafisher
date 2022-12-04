import numpy as np
from skimage.exposure import adjust_gamma, equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.measure import label, regionprops
from skimage.measure._regionprops import RegionProperties
from skimage.morphology import binary_erosion, disk, binary_opening, binary_dilation, binary_closing

from .get_head import should_be_rotated, get_head, get_two_sides_img
from ..models import BoundingBox, InputImage
from ..utils import msg, keep_2_largest_object


def get_eyes(input_img: InputImage) -> InputImage:
    """
    Segments potential eye region(s) from convex mask of fish

    :param input_img: InputImage object the convex fish mask calculated

    :rtype: InputImage object with filled 'fish_props.eyes' property
    """
    mask = input_img.fish_props.mask.og
    cropped_mask = input_img.fish_props.mask.cropped
    cropped_og = input_img.fish_props.cropped_og

    masked = adjust_gamma((unsharp_mask(cropped_og, radius=2) * mask), gamma=2)

    # Rotating if width < height
    if should_be_rotated(cropped_mask):
        input_img.fish_props.rotated = True
        mask = np.transpose(mask)
        cropped_mask = np.transpose(cropped_mask)
        cropped_og = np.transpose(cropped_og)
        masked = np.transpose(masked)

    # Splitting image and masks in half
    sides = get_two_sides_img(masked)
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
    th = (head < mean * 0.28) * head_mask  # thresholding

    th = eye_spy(th)  # filtering out possible eye objects
    th = remove_hind_objects(th, side)  # removing objects on the hind side of the head part

    are_eyes, eye_count = check_eyes(th)

    if 5 >= eye_count > 2:  # If there are only a few objects present, we only keep the 2 largest
        msg(f"Found more than 2 possible eyes found: {eye_count} -> keeping the 2 largest")
        th = keep_2_largest_object(th)
        are_eyes, eye_count = check_eyes(th)

    if eye_count == 1:
        msg("Only found one eye!")
        input_img.fish_props.has_eyes = True
        input_img.success = True
    elif eye_count == 2:
        msg("Found 2 eyes!")
        th = convex_eyes(th)  # Keeping the convex shapes of the eyes if there is only 2
        input_img.fish_props.has_eyes = True
        input_img.success = True
    elif eye_count == 0:
        msg("No eyes found!")
        input_img.fish_props.has_eyes = False
        input_img.success = False
        input_img.fish_props.eyes = np.zeros_like(mask)
    else:
        msg(f"Found more than 5 possible eyes found: {eye_count}")
        input_img.fish_props.has_eyes = False
        input_img.success = False
        input_img.fish_props.eyes = np.zeros_like(mask)

    # If eyes were found
    if input_img.fish_props.has_eyes:
        th = binary_dilation(th, disk(3))  # Dilating previously eroded objects

        input_img.fish_props.eyes = th  # Storing eyes

        # Adding eyes to the cropped mask
        head_with_eyes = np.logical_or(th, head_cropped_mask)
        if side == "l":
            cropped_mask = np.concatenate([head_with_eyes, sides_cropped_mask[1]], axis=1)
            th = np.concatenate([th, np.zeros_like(sides_cropped_mask[1])], axis=1)
        elif side == "r":
            cropped_mask = np.concatenate([sides_cropped_mask[0], head_with_eyes], axis=1)
            th = np.concatenate([np.zeros_like(sides_cropped_mask[0]), th], axis=1)

    # Storing masks and thresholded images
    input_img.fish_props.mask.cropped = cropped_mask
    input_img.fish_props.cropped_og = cropped_og
    input_img.fish_props.eyes = th

    # Rotating back previously rotated masks
    if input_img.fish_props.rotated:
        input_img.fish_props.mask.og = input_img.fish_props.mask.og.transpose()
        input_img.fish_props.mask.cropped = input_img.fish_props.mask.cropped.transpose()
        input_img.fish_props.cropped_og = input_img.fish_props.cropped_og.transpose()
        input_img.fish_props.eyes = input_img.fish_props.eyes.transpose()

    # Creating fish mask relative to the well
    mask_in_well = np.zeros_like(input_img.well_props.mask.cropped)
    bbox = input_img.fish_props.bounding_box_well
    mask_in_well[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = input_img.fish_props.mask.cropped

    mask_in_well = binary_closing(mask_in_well, disk(13))  # Closing holes and smoothing edges

    input_img.fish_props.mask.og = mask_in_well
    input_img.fish_props.mask.masked = mask_in_well * input_img.well_props.mask.cropped_masked

    # Updating cropped ones
    bbox = input_img.fish_props.bounding_box_well
    input_img.fish_props.mask.cropped = bbox.bound_img(input_img.fish_props.mask.og)
    input_img.fish_props.mask.cropped_masked = bbox.bound_img(input_img.fish_props.mask.masked)

    # Making sure that eye correctly stored
    if input_img.fish_props.eyes.shape != input_img.fish_props.mask.cropped.shape:
        if not input_img.fish_props.has_eyes:
            input_img.fish_props.eyes = np.zeros_like(input_img.fish_props.mask.cropped.shape)
            return input_img
        else:
            raise Exception(
                f'hazard'
                f'input_img.fish_props.eyes.shape != input_img.fish_props.mask.cropped.shape ->'
                f' {input_img.fish_props.eyes.shape} != {input_img.fish_props.mask.cropped.shape}')
            # input_img.fish_props.has_eyes = False
            # input_img.success = False

    return input_img


def eye_spy(fish: np.ndarray):
    msg("Searching for eye regions")
    fish = binary_erosion(fish, disk(3))
    fish = binary_opening(fish, disk(3))
    props = regionprops(label(fish))
    props = list(filter(eye_criteria, props))

    rem = put_rprops_on_empty(fish.shape, props)
    return rem


def eye_criteria(x: RegionProperties) -> bool:
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


def convex_eyes(bin_img: np.ndarray) -> np.ndarray:
    props = regionprops(label(bin_img))
    if len(props) == 2:
        return put_rprops_on_empty(bin_img.shape, props, True)
    print(f"{len(props)} eyes cannot be turned convex")
    return bin_img


def put_rprops_on_empty(shape: (int, int), rprops: list[RegionProperties], convex: bool = False):
    rem = np.zeros(shape)
    for i_, r in enumerate(rprops):
        bbox = BoundingBox()
        bbox.set(r.bbox)
        if not convex:
            rem[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = r.image_filled
        else:
            rem[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = r.image_convex
    return rem
