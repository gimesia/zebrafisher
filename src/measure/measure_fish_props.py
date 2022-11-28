import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing, disk

from .extract_to_csv import writerow_from_inputimage, put_analysis_result_into_csv
from src.models import InputImage
from src.utils import get_bounding_box_obj


def measure_fish_props(input_img: InputImage) -> InputImage:
    input_img.measurements.calculate_resolution(input_img.well_props.radius)  # Calculating resolution

    if not input_img.fish_props.has_fish or not input_img.fish_props.has_eyes:
        # write in csv
        return input_img

    input_img = measure_eyes(input_img)  # Measuring eyes
    input_img = measure_endpoints(input_img)  # Measuring endpoints

    put_analysis_result_into_csv(input_img)

    # TODO imsave into src/images/out

    return input_img


def measure_eyes(input_img: InputImage) -> InputImage:
    props = regionprops(label(input_img.fish_props.eyes))

    if len(props) == 1:
        # Temporary until watershed is implemented
        input_img.measurements.eye1_diameter_major = props[0].axis_minor_length

    if len(props) == 2:
        input_img.measurements.eye1_diameter_major = props[0].axis_major_length
        input_img.measurements.eye2_diameter_major = props[1].axis_major_length

    return input_img


def measure_endpoints(input_image: InputImage) -> InputImage:
    mask = input_image.fish_props.mask.cropped
    start_size = np.zeros_like(mask)

    mask = binary_closing(mask, disk(15))
    props = regionprops(label(mask))

    input_image.measurements.orientation = props[0].orientation

    bbox = get_bounding_box_obj(mask)

    return input_image
