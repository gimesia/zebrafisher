from scipy.ndimage import binary_fill_holes
from scipy.ndimage import binary_fill_holes
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.filters.ridges import meijering
from skimage.morphology import disk, binary_closing, convex_hull_image, remove_small_objects

from src.filters import yen_thresholding, yen_th
from src.models import InputImage
from src.utils import keep_largest_object, get_filled_object, keep_largest_object_convex, get_bounding_box, \
    get_bounding_box_obj
from src.utils.terminal_msg import msg, show_img
from .is_fish import is_fish
from .remove_background import remove_background


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")

    input_img = remove_background(input_img)

    input_img = yen_thresholding(input_img)
    filled = binary_closing(binary_fill_holes(input_img.processed), disk(10)).astype(float)
    input_img.processed = filled * input_img.well_props.mask.cropped

    input_img.fish_props.mask.og = convex_hull_image(input_img.processed).astype(
        float)  # Fish hull ready to be analyzed further
    input_img.processed = input_img.fish_props.mask.og

    index = 1
    while not is_fish(input_img.fish_props.mask.og):
        print(f"Refine fish convex hull #{index}")
        input_img = refine_oversized_hull(input_img, step=index)
        if index > 5:
            break
        else:
            index += 1

    masked = input_img.fish_props.mask.og * input_img.well_props.mask.cropped_masked

    input_img.fish_props.bounding_box = get_bounding_box_obj(masked)
    input_img.fish_props.mask.masked = masked
    input_img.processed = masked

    # input_img = get_fish_convex_mask(input_img)
    # input_img = refine_fish_convex_mask(input_img)
    # input_img = refine_fish_mask(input_img)

    return input_img


def refine_oversized_hull(input_img: InputImage, step=0) -> InputImage:
    msg("Refining convex hull of fish")
    hull = input_img.fish_props.mask.og
    well_masked = input_img.well_props.mask.cropped_masked

    unsharp_masked = unsharp_mask(hull * well_masked, amount=20 + (step * 0.5), radius=2)

    meijered = meijering(unsharp_masked)

    y = yen_th(meijered)

    proc = y * hull

    klo = keep_largest_object_convex(proc)  # binary_dilation(proc, disk(5)))
    input_img.fish_props.mask.og = klo

    return input_img
