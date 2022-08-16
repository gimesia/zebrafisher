import numpy as np

from src.filters import normalize_0_255
from src.fish.find_fish_props import find_fish_props
from src.models import InputImage
from src.utils.terminal_msg import msg, show_img, show_multiple_img
from src.well.find_well_props import find_well_props


def image_processing_pipeline(filename: str) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    # Normalizing intensity
    input_img.processed = normalize_0_255(input_img.processed)

    # Converting back to unsigned integers Double -> UInt8
    input_img.processed = np.uint8(input_img.processed)

    # Find well script
    input_img = find_well_props(input_img)
    if input_img.well_props.is_well:
        msg("FOUND WELL!")
    else:
        Warning("No well was found!")

    # Find fish script
    input_img = find_fish_props(input_img)
    if input_img.fish_props.is_fish:
        msg("FOUND FISH!")
    else:
        Warning("No fish was found!")

    return input_img


if __name__ == '__main__':
    _1 = image_processing_pipeline("zf1.jpg")
    """_2 = image_processing_pipeline("zf2.jpg")
    _3 = image_processing_pipeline("zf3.jpg")
    _4 = image_processing_pipeline("zf4.jpg")
    _5 = image_processing_pipeline("zf5.jpg")
    _6 = image_processing_pipeline("zf6.jpg")"""
    show_multiple_img(
        [_1.fish_props.mask.cropped_masked]) # _2.fish_props.mask.cropped_masked, _3.fish_props.mask.cropped_masked, _4.fish_props.mask.cropped_masked, _5.fish_props.mask.cropped_masked, _6.fish_props.mask.cropped_masked])
