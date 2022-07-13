import cv2 as cv
import numpy as np


def msg(title: str, data: any):
    print(f"{title}\n\n")
    print(f"{data}\n\n\n\n")


def show_img(image: np.ndarray, title="Image"):
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyAllWindows()
