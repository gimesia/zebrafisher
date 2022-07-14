from InputImage import InputImage
from local_contrast_enhancement import local_contrast_enhancement
from get_mask_for_correction import get_mask_for_correction
from robust_homomorphic_surface_fitting import robust_homomorphic_surface_fitting


def illumination_correction(input_img: InputImage) -> InputImage:
    input_img = local_contrast_enhancement(input_img)

    input_img = get_mask_for_correction(input_img)

    input_img = robust_homomorphic_surface_fitting(input_img, input_img.well_props.mask)

    return input_img
