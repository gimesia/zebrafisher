import numpy as np
from skimage.measure import regionprops_table, regionprops, label
from skimage.morphology import square, binary_erosion

from src.fish import sobel, yen_th
from src.filters.sharpen_img import sharpen_img
from src.models import InputImage
from src.terminal_msg import msg


def correct_fish_mask(input_img: InputImage):
    msg("Fish mask too big! Correcting mask!")
    bbox = input_img.fish_props.bounding_box
    og_mask = input_img.fish_props.mask.og.copy()
    new_mask = binary_erosion(og_mask, square(5)).astype(np.uint8)

    img = input_img.processed.copy()
    img = sharpen_img(img)
    img = sobel(img, equalized=False)
    yen = yen_th(img)

    labeled = label(yen)
    props = regionprops_table(labeled, properties=('area', 'label'))

    max_area = props['area'].max()
    max_index = np.where(props['area'] == max_area)[0][0]

    region_props = regionprops(labeled)[max_index]

    new_bbox = region_props.bbox
    print(f'{img.dtype} &{region_props.image_convex.dtype}')
    img[new_bbox[0]:new_bbox[2], new_bbox[1]: new_bbox[3]] = region_props.image_convex
    input_img.fish_props.mask.og = region_props.image_convex
    # input_img.fish_props.bounding_box = BoundingBox(new_bbox[0], new_bbox[1], new_bbox[2], new_bbox[3])

    return input_img
