import numpy as np
from scipy.signal import wiener
from skimage.morphology import disk, opening
import cv2 as cv

from src.fish.get_possible_fish import get_possible_fish
from src.fish.guassian_hpf import gaussian_high_pass_filter
from src.fish.yen_thresholding import yen_thresholding
from src.models import InputImage, EXAMPLE_IMG
from src.terminal_msg import show_img, msg


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")
    filtered_img = input_img.processed

    input_img = gaussian_high_pass_filter(input_img)

    input_img = yen_thresholding(input_img)

    # filtered_img = wiener(input_img.processed, (5, 5))

    # input_img = get_possible_fish(input_img)

    return input_img


""" segmented_fish_og_size = np.zeros(input_img.size())
 bounding_box = input_img.well_props.bounding_box
 og_mask = input_img.well_props.mask.og
 cropped_mask = input_img.well_props.mask.cropped

 # input_img.processed = normalize_intensity_range(input_img.processed, (0, 1))

 # illCorrected = homomorphic(input_img.processed, 2, 0.015, 2, 1);

 # filteredImg = rangefilt(illCorrected);

 # croppedFilteredImg = filteredImg(bBox(2) : bBox(4), bBox(1) : bBox(3));
 # croppedFilteredImg = wiener2(croppedFilteredImg, [30 30]);

 # originalCropped = image(bBox(2) : bBox(4), bBox(1) : bBox(3));

 # % erzekeny a kernel meretere
 # T = adaptthresh(croppedFilteredImg, 0.95, 'ForegroundPolarity', 'dark', ...
 #     'Statistic', 'gaussian', 'NeighborhoodSize', 2*floor(size(croppedFilteredImg)/14)+1);

 # bin_filtered = imbinarize(croppedFilteredImg, T);
 # bin_filtered(maskCropped == 0) = 0;

 input_img.binary = bin_filtered

 input_img = _get_possible_fish(input_img)

 if input_img.fish_props.is_fish:
     x1 = input_img.fish_props.bounding_box.x1
     y1 = input_img.fish_props.bounding_box.y1
     x2 = input_img.fish_props.bounding_box.x2
     y2 = input_img.fish_props.bounding_box.y2

     # temp = input_img.fish_props.filled_fish
     # if input_img.fish_props.rotated:
     #    temp = rotate(temp, 90)

     # segmented_fish_og_size[y1:y2, x1:x2] = temp

 structuring_element = disk(2)

 segmented_fish_og_size = opening(segmented_fish_og_size, structuring_element)
 # segmentedFishOrigSize = bwareafilt(segmentedFishOrigSize, 1);

 # possFishProps.segmentedOrigSizeFish = segmentedFishOrigSize;"""

if __name__ == '__main__':
    a = EXAMPLE_IMG
    find_fish_props(a)
