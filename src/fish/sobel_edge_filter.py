import numpy as np


def sobel_edges(img: np.ndarray):
    ddepth = cv.CV_16S
    grad_x = cv.Sobel(src=img, ddepth=ddepth, dx=1, dy=0, ksize=3)
    grad_y = cv.Sobel(src=img, ddepth=ddepth, dx=0, dy=1, ksize=3)