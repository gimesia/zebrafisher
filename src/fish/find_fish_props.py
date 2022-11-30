from .get_eyes import get_eyes
from .get_possible_fish import get_possible_fish
from .is_fish import is_fish
from ..models import InputImage
from ..utils import msg


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    input_img = get_possible_fish(input_img)

    if not is_fish(input_img.fish_props.mask.cropped, input_img.well_props.mask.cropped):
        input_img.fish_props.has_fish = False
        input_img.success = False
        msg("No possible fish was found")
        return input_img
    else:
        input_img.fish_props.has_fish = True

    input_img = get_eyes(input_img)
    if not input_img.fish_props.has_eyes:
        input_img.success = False
        msg("No possible eyes were found")
        return input_img

    return input_img
