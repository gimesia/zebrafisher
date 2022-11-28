import os

from src.fish import find_fish_props
from src.measure.measure_fish_props import measure_fish_props
from src.models import InputImage
from src.utils import normalize_0_255
from src.utils.terminal_msg import msg, show_img, show_multiple_img
from src.well.find_well_props import find_well_props


def image_processing_pipeline(filename: str) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    if not input_img.width or not input_img.height:
        msg("InputImage failed to load")
        return input_img

    input_img.processed = normalize_0_255(input_img.processed)  # Normalizing intensity

    # Find well script
    input_img = find_well_props(input_img)
    if input_img.well_props.has_well:
        msg("FOUND WELL!")

        # Find fish script
        input_img = find_fish_props(input_img)
        if input_img.fish_props.has_fish and input_img.fish_props.has_eyes:
            input_img.success = True
            msg("FOUND FISH & EYE(S)!")
        else:
            input_img.success = False
    else:
        msg("No well was found!")
        input_img.success = False

    # Measure segmented fish
    input_img = measure_fish_props(input_img)

    return input_img


def run_pipeline_for_all_images(popups: bool = False):
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, "images", "in"))
    fish_names = os.listdir()
    os.chdir(cwd)

    for i, name in enumerate(fish_names):
        print(f'# Running image processing algorithm on file: {name}')
        fish = image_processing_pipeline(name)
        if fish.success:
            print("\n\n")
            print("ANALYSIS SUCCESSFUL")
            print("\n\n")
            if popups:
                show(fish)
        else:
            print("\n\n")
            print("ANALYSIS FAILED")
            print("\n\n")

    print('fin.')


def show(inp: InputImage):
    # show_img(inp.well_props.mask.cropped_masked, "inp.well_props.mask.cropped_masked")
    # show_img(inp.fish_props.mask.og, 'inp.fish_props.mask.og')
    #show_img(inp.fish_props.cropped_og, 'inp.fish_props.cropped_og')
    #show_img(inp.og, 'inp.fish_props.cropped_og')
    #show_img(inp.fish_props.mask.cropped, 'inp.fish_props.mask.cropped')
    #show_img(inp.fish_props.eyes.astype(float), 'eyes')


if __name__ == '__main__':
    run_pipeline_for_all_images(True)
    print('fin')
