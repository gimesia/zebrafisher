import numpy as np

from src.filters import normalize_0_255
from src.fish.find_fish_props import find_fish_props
from src.models import InputImage
from src.utils.terminal_msg import msg, show_img
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
    res = image_processing_pipeline("zf1.jpg")
    show_img(res.processed)
    show_img(res.fish_props.mask.masked)
    show_img(res.fish_props.mask.cropped)
