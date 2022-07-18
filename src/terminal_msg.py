import cv2 as cv
import numpy as np


def msg(title: str, data: any = None):
    print(f"{title}\n\n")
    print(f"{data}\n")
    print("_____________________________________________________________")


def show_img(image: np.ndarray, title="Image"):
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyAllWindows()
