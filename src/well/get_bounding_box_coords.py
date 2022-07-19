from skimage.measure import regionprops

from src.InputImage import InputImage
from src.terminal_msg import msg


def get_bounding_box_coords(input_img: InputImage) -> InputImage:
    msg("Get bounding box")
    actual_height, actual_width = input_img.height, input_img.width

    # input_img.processed = bwareafilt(input_img.processed)

    props = regionprops(input_img.processed)
    # (min_row, min_col, max_row, max_col)
    [x1, y1, x2, y2] = props[0].bbox

    if actual_height <= y2:
        y2 = y2 - 1

    if actual_width <= x2:
        x2 = x2 - 1

    input_img.well_props.bounding_box.x1 = x1
    input_img.well_props.bounding_box.y1 = y1
    input_img.well_props.bounding_box.x2 = x2
    input_img.well_props.bounding_box.y2 = y2

    return input_img


if __name__ == "__main__":
    a = InputImage("zf.png")
    get_bounding_box_coords(a)
    print(a.well_props.bounding_box)
