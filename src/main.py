import os

import cv2
import numpy as np

from src.fish import find_fish_props
from src.measure import create_result_image
from src.measure.measure_fish_props import measure_fish_props
from src.models import InputImage
from src.models.Timer import Timer
from src.utils import normalize_0_255
from src.utils.terminal_msg import msg, show_img
from src.well.find_well_props import find_well_props


def image_processing_pipeline(filename: str, save: bool = True) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    if not input_img.width or not input_img.height:
        msg("InputImage failed to load")
        return input_img

    input_img.processed = normalize_0_255(input_img.processed).astype(np.uint8)  # Normalizing intensity

    # Find well script
    well_timer = Timer()
    input_img = find_well_props(input_img)
    well_timer.stop()

    if input_img.well_props.has_well:
        msg("FOUND WELL!")

        # Find fish script
        fish_timer = Timer()
        input_img = find_fish_props(input_img)
        fish_timer.stop()

        if input_img.fish_props.has_fish and input_img.fish_props.has_eyes:
            input_img.success = True
            msg("FOUND FISH & EYE(S)!")
        elif input_img.fish_props.has_fish and not input_img.fish_props.has_eyes:
            msg("FOUND FISH, BUT NO EYE(S)!")
            input_img.success = False
        else:
            msg("NO FISH WAS FOUND!")
            input_img.success = False
    else:
        msg("NO WELL WAS FOUND!")
        input_img.success = False

    # Measure segmented fish
    measurements_timer = Timer()
    input_img = measure_fish_props(input_img)
    measurements_timer.stop()

    input_img.measurements.times = [well_timer.duration.seconds, fish_timer.duration.seconds,
                                    measurements_timer.duration.seconds]

    # Save result image
    if input_img.success and save:
        res = create_result_image(input_img)
        show_img(res, f"{input_img.name}: Lines")

        cwd = os.getcwd()
        os.chdir(os.path.join(cwd, "images", "out"))
        cv2.imwrite(f"{input_img.name.split('.')[0]}_processed.jpg", res)
        os.chdir(cwd)

    return input_img


def run_pipeline_for_all_images(save: bool = False, popups: bool = False):
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, "images", "in"))  # Changing working directory to read filenames
    fish_names = os.listdir()  # Read filenames
    os.chdir(cwd)  # Changing directory back to original

    fish_names = list(filter(lambda x: len(x.split(".")) > 1, fish_names))  # filtering out non-file names

    # Break the pipeline
    if not len(fish_names):
        print("No image files found in \'images/in\'")
        return

    for i, name in enumerate(fish_names[::]):
        print(f"# Running image processing algorithm #{i + 1} on file: {name}")
        try:
            fish = image_processing_pipeline(name)
        except():
            print("Input image file is not the right format (.jpg, .tiff, .czi, .png!")

        if fish.success:
            print("\n")
            print("ANALYSIS SUCCESSFUL")
            print("\n\n")
            if popups:
                show(fish)
        else:
            print("\n")
            print("ANALYSIS FAILED")
            print("\n\n")

    print("fin.")


def show(inp: InputImage):
    # show_img(inp.well_props.mask.cropped_masked, "inp.well_props.mask.cropped_masked")
    # show_img(inp.fish_props.mask.og, 'inp.fish_props.mask.og')
    # show_img(inp.fish_props.cropped_og, 'inp.fish_props.cropped_og')
    # show_img(inp.og, 'inp.fish_props.cropped_og')
    # show_img(inp.fish_props.mask.cropped, 'inp.fish_props.mask.cropped')
    # show_img(inp.fish_props.eyes.astype(float), 'eyes')
    return


if __name__ == "__main__":
    run_pipeline_for_all_images(True)
    print("fin")
