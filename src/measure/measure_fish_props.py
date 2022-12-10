from skimage.measure import label, regionprops

from .extract_to_csv import measurements_to_csv
from ..models import InputImage


def measure_fish_props(input_img: InputImage) -> InputImage:
    """
    Measure all quantitative properties of segmented areas

    :param input_img: InputImage object
    :return: InputImage object with filled .measurement property
    """
    input_img.measurements.calculate_resolution(input_img.well_props.radius)  # Calculating resolution

    if not input_img.fish_props.has_fish:
        if not input_img.fish_props.has_eyes:
            measurements_to_csv(input_img)  # Save measurements to destination csv
            return input_img

        input_img = measure_axes(input_img)  # Measuring endpoints
        return input_img

    input_img = measure_eyes(input_img)  # Measuring eyes
    input_img = measure_axes(input_img)  # Measuring endpoints

    measurements_to_csv(input_img)  # Save measurements to destination csv

    return input_img


def measure_eyes(input_img: InputImage) -> InputImage:
    """
    Measure eye count and diameter

    :param input_img: InputImage object
    :return: InputImage object with filled properties in regarding the eyes
    """
    props = regionprops(label(input_img.fish_props.eyes))

    if len(props) == 1:
        # Temporary until watershed is implemented
        input_img.measurements.eye1_diameter_major = props[0].axis_minor_length

    if len(props) == 2:
        input_img.measurements.eye1_diameter_major = props[0].axis_major_length
        input_img.measurements.eye2_diameter_major = props[1].axis_major_length

    return input_img


def measure_axes(input_img: InputImage) -> InputImage:
    """
    Measure length of axes and their ratio

    :param input_img: InputImage object
    :return: InputImage object with filled properties regarding the axes
    """
    mask = input_img.fish_props.mask.cropped
    props = regionprops(label(mask))

    major = props[0].axis_major_length
    minor = props[0].axis_minor_length

    input_img.measurements.axis_major = major
    input_img.measurements.axis_minor = minor
    input_img.measurements.calculate_axes_ratio()
    input_img.measurements.area = props[0].area

    return input_img
