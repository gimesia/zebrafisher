from skimage.measure import label, regionprops

from .extract_to_csv import put_analysis_result_into_csv
from ..models import InputImage


def measure_fish_props(input_img: InputImage) -> InputImage:
    input_img.measurements.calculate_resolution(input_img.well_props.radius)  # Calculating resolution

    if not input_img.fish_props.has_fish or not input_img.fish_props.has_eyes:
        # write in csv
        put_analysis_result_into_csv(input_img)
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
    props = regionprops(label(mask))

    major = props[0].axis_major_length
    minor = props[0].axis_minor_length

    input_image.measurements.axis_major = major
    input_image.measurements.axis_minor = minor
    input_image.measurements.calculate_axes_ratio()
    input_image.measurements.area = props[0].area

    return input_image
