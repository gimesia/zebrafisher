import cv2
import numpy as np

from src.utils.terminal_msg import show_img


def get_mean_of_cols_for_sides(bin_img: np.ndarray, rotated=False):
    show_img(bin_img.astype(float))
    print(bin_img.shape)
    if rotated:
        print("Rotated fish for head analysis!")
        bin_img = np.transpose(bin_img)
        show_img(bin_img.astype(float))
    print(bin_img.shape)

    h, w = bin_img.shape
    ch, cw = int(h / 2), int(w / 2)

    left_side = bin_img[:, 0:cw]
    right_side = bin_img[:, cw:]

    show_img(left_side.astype(float))
    show_img(right_side.astype(float))
    left_sum = np.sum(left_side, axis=0)  # Sum of columns
    right_sum = np.sum(right_side, axis=0)  # Sum of columns
    return [np.mean(left_sum), np.mean(right_sum)]  # Means of the col sums


if __name__ == '__main__':
    # WIP
    a = cv2.imread('output.png', 0)
    b = get_head_position(a, (a.shape[0] > a.shape[1]))
    print(b)
