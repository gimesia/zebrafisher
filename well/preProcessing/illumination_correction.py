from InputImage import InputImage
from well.preProcessing.local_contrast_enhancement import local_contrast_enhancement


def illumination_correction(input_img: InputImage):
    corr = local_contrast_enhancement(input_img)


    return
