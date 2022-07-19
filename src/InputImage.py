from typing import Tuple

import cv2 as cv
import numpy as np


class FishProperties:
    def __init__(self):
        self.fish = None


class BoundingBox:
    def __init__(self):
        self.x1: int = None
        self.y1: int = None
        self.x2: int = None
        self.y2: int = None

    def __str__(self):
        return f"x1: {self.x1},\ny1: {self.y1},\nx2: {self.x2},\ny2: {self.y2}"


class WellProperties:
    def __init__(self):
        self.min_circle: int = None
        self.max_circle: int = None
        self.center: tuple[int, int] = None
        self.radius: int = None
        self.found_well: bool = None
        self.mask: np.ndarray = None
        self.bounding_box: BoundingBox = BoundingBox()


class InputImage:
    def __init__(self, filename):
        path = r'C:\Users\gimesia\Documents\PROJEKT\zebrafish_pipenv\src\images'  # NEED TO BE CHANGED IF RAN FROM ANOTHER COMPUTER
        path = path + "\\" + filename

        self.og: np.ndarray = cv.imread(path)
        self.processed: np.ndarray = cv.imread(path, 0)  # Already processes it to gray
        self.height: int = 0
        self.width: int = 0
        self.well_props: WellProperties = WellProperties()
        try:
            self.set_size()
        except:
            raise Exception("Image loading failed")

    def set_size(self):
        self.height = self.og.shape[0]
        self.width = self.og.shape[1]

    def size(self) -> tuple[int, int]:
        return self.height, self.width


PROTOTYPE_IMG = InputImage("zf2.jpg")

if __name__ == '__main__':
    img = PROTOTYPE_IMG
    print(img.size())
