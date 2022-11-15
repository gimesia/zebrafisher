from scipy.signal import wiener
from skimage.exposure import equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.morphology import binary_closing, disk

from .rangefilter import range_filter
from .remove_container import get_meniscus_effect, iterative_dilation
from ..models import InputImage, BoundingBox
from ..utils import keep_largest_object, keep_largest_object_convex, get_bounding_box_obj, normalize_0_1, \
    normalize_0_255, yen_th, msg


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    msg("Applying range-filter")
    eq = unsharp_mask(input_img.processed, radius=2)  # Sharpening
    rng_filter = range_filter(eq, input_img.well_props.mask.cropped)  # Range-filter
    normalized = normalize_0_1(rng_filter)  # Normalizing for wiener
    normalized = equalize_adapthist(normalized)  # Equalizing

    msg("Applying wiener-filter")
    input_img.processed = wiener(normalized, mysize=30)  # denoising with wiener filter
    norm = normalize_0_255(unsharp_mask(input_img.processed, radius=2))  # Normalizing and sharpening for thresholding

    msg("Applying adaptive-threshold")
    binary_img = yen_th(norm)  # Yen-thresholding
    # show_img(binary_img, 'th')

    # Get possible fish
    binary_img = binary_closing(binary_img, disk(3))
    # show_img(binary_img, 'closing')

    msg("Removing meniscus")
    meniscus = get_meniscus_effect(binary_img, input_img.well_props.mask.cropped).astype(float)
    binary_img = binary_img - meniscus
    # show_img(binary_img, 'menisc')

    msg("Keeping only the possible fish")
    binary_img = keep_largest_object(binary_img, filled=True).astype(bool)
    # show_img(binary_img, 'klo')

    # Creating convex hull for the fish
    convex_mask = keep_largest_object_convex(binary_img)  # maybe other method is fine
    convex_mask = iterative_dilation(convex_mask, 6, disk(5))

    input_img.fish_props.mask.og = convex_mask  # Storing as og mask (relative to the well)
    # show_img(convex, 'convex')

    # Inner bbox (fish's bbox inside well's bbox)
    bbox_well_relative = get_bounding_box_obj(convex_mask)
    input_img.fish_props.bounding_box_well = bbox_well_relative
    bbox_og_relative = BoundingBox(input_img.well_props.bounding_box.x1 + bbox_well_relative.x1,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y1,
                                   input_img.well_props.bounding_box.x1 + bbox_well_relative.x2,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y2)

    # Bbox relative to original image
    input_img.fish_props.bounding_box_og = bbox_og_relative

    # Storing image of original image cropped to display only the fish
    input_img.fish_props.cropped_og = input_img.og[
                                      bbox_og_relative.x1:bbox_og_relative.x2,
                                      bbox_og_relative.y1:bbox_og_relative.y2
                                      ]

    input_img.fish_props.mask.cropped = bbox_well_relative.bound_img(binary_img)
    input_img.processed = binary_img

    return input_img
