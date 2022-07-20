import numpy as np

from src.InputImage import InputImage, EXAMPLE_IMG
from src.well.normalize_intensity_range import normalize_intensity_range


def find_fish_props(input_img: InputImage) -> InputImage:
    # TODO! Maybe I will need to start over from the og image based on matlab

    segmented_fish_og_size = np.zeros(input_img.size())
    bounding_box = input_img.well_props.bounding_box
    og_mask = input_img.well_props.mask.og
    cropped_mask = input_img.well_props.mask.cropped

    # input_img.processed = normalize_intensity_range(input_img.processed, (0, 1))

    return input_img


if __name__ == '__main__':
    a = EXAMPLE_IMG
    print(a)
