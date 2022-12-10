import os

import numpy as np

from src.fish import find_fish_props
from src.measure import save_result_image, measure_fish_props, writerow_empty
from src.models import InputImage, Timer
from src.utils import normalize_0_255, msg
from src.well.find_well_props import find_well_props


def image_processing_pipeline(filename: str, save: bool = True, popups: bool = False) -> InputImage:
    """
    Zebra-fish embryo morphological analysis pipeline

    :param filename: name of the input file (must be in 'src/images/in')
    :param save: If True result images are saved into 'src/images/out'
    :param popups: If True a popup window is shown after a successful pipeline
    :return: InputImage object with filled properties
    """
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    if not input_img.width or not input_img.height:
        msg("InputImage failed to load")
        return input_img

    input_img.processed = normalize_0_255(input_img.processed).astype(np.uint8)  # Normalizing intensity

    # Find well script
    well_timer = Timer()  # timer start
    input_img = find_well_props(input_img)
    well_timer.stop()  # timer stop

    if input_img.well_props.has_well:
        msg("FOUND WELL!")

        # Find fish script
        fish_timer = Timer()  # timer start
        input_img = find_fish_props(input_img)
        fish_timer.stop()  # timer stop

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
    measurements_timer = Timer()  # timer start
    input_img = measure_fish_props(input_img)
    measurements_timer.stop()  # timer stop

    input_img.timer.stop()

    # Save Times
    # input_img.measurements.times =
    # [well_timer.duration, fish_timer.duration, measurements_timer.duration,input_img.timer.duration]

    # Save result image
    if input_img.success and save:
        save_result_image(input_img, popups)

    return input_img


def run_pipeline_for_all_images(save: bool = False, batch_name: str = "", popups: bool = False):
    """
    Runs image processing pipeline on all files in 'src\\images\\in' or in its 1 deep folders
    :param save: If True result images are saved
    :param batch_name: Name of the analyzed batch
    :param popups: If True the result images are shown in a popup window
    """
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, "images", "in"))  # Changing working directory to read filenames
    fish_names = os.listdir()  # Read filenames
    os.chdir(cwd)  # Changing directory back to original

    # fish_names = list(filter(lambda x: 3 > len(x.split(".")) > 1, fish_names))  # filtering out non-file names
    fish_names = get_names()
    # Break the pipeline
    if not len(fish_names):
        print("No image files found in \'images/in\'")
        return

    for i, name in enumerate(fish_names[::]):
        print(f"# Running image processing algorithm #{i + 1} on file: {name}")
        try:
            fish = image_processing_pipeline(name, save, popups)
        except():
            print("Input image file is not the right format (.jpg, .tiff, .czi, .png!")

        if fish.success:
            print("\n")
            print("ANALYSIS SUCCESSFUL")
            print("\n\n")

        else:
            print("\n")
            print("ANALYSIS FAILED")
            print("\n\n")

        # measurement_times_csv(
        #   [batch_name, fish.name, fish.measurements.times[0], fish.measurements.times[1], fish.measurements.times[2],
        #   fish.measurements.times[3]])

    writerow_empty(f"END OF BATCH {batch_name}")
    print("fin.")


def get_names() -> list[str]:
    """
    Gets the filenames in src/images/in and 1 deep directories

    :return: list of the filenames
    """
    cwd = os.getcwd()
    path = os.path.join(cwd, "images", "in")
    os.chdir(path)  # Changing working directory to read filenames

    fish_names = os.listdir()  # Read filenames
    dirs = list(filter(lambda x: len(x.split(".")) == 1, fish_names))  # Filter out names
    files = []  # Files

    for dir in dirs:
        dir_files = os.listdir(os.path.join(path, dir))
        for f in dir_files:
            files.append(f'{dir}\\{f}')

    if len(dirs) == 0:
        files = list(filter(lambda x: len(x.split(".")) == 2, fish_names))

    os.chdir(cwd)  # Changing directory back to original
    return files


if __name__ == "__main__":
    run_pipeline_for_all_images(save=True, batch_name="", popups=True)
