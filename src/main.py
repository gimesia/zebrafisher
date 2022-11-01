import numpy as np

from src.filters import normalize_0_255
from src.fish import find_fish_props
from src.models import InputImage
from src.utils.terminal_msg import msg, show_img, show_multiple_img
from src.well.find_well_props import find_well_props


def image_processing_pipeline(filename: str) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)
    input_img.processed = normalize_0_255(input_img.processed)  # Normalizing intensity

    # Find well script
    input_img = find_well_props(input_img)
    if input_img.well_props.has_well:
        msg("FOUND WELL!")
    else:
        raise Exception("No well was found!")

    # Find fish script
    input_img = find_fish_props(input_img)
    if input_img.fish_props.has_fish:
        msg("FOUND FISH!")
    else:
        pass
    #   raise Exception("No fish was found!")

    return input_img


if __name__ == '__main__':
    _1 = image_processing_pipeline("zf8.jpg")
    print('fin')
