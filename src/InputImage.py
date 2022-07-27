import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


class Measures:
    def __int__(self):
        self.well_roi: [int, int, int, int] = None
        self.fish_roi = None
        self.tail_length = None
        self.eye_diameter = None
        self.head_endpoint = None
        self.tail_endpoint = None


class FishProperties:
    def __init__(self):
        self.is_fish: bool = None
        self.bounding_box: BoundingBox = BoundingBox()
        self.rotated: bool = None
        self.og_segmented: np.ndarray = None
        self.container = None
        self.mod_cont = None


class BoundingBox:
    def __init__(self, x1: int = None, y1: int = None, x2: int = None, y2: int = None):
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2

    def get(self) -> [int, int, int, int]:
        return [self.x1, self.y1, self.x2, self.y2]

    def __str__(self):
        return f"x1: {self.x1},\ny1: {self.y1},\nx2: {self.x2},\ny2: {self.y2}"


class Mask:
    def __int__(self):
        self.og: np.ndarray = None
        self.cropped: np.ndarray = None
        self.gray: np.ndarray = None
        self.cropped_gray: np.ndarray = None


class WellProperties:
    def __init__(self):
        self.min_circle: int = None
        self.max_circle: int = None
        self.center: tuple[int, int] = None
        self.radius: int = None
        self.bounding_box: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()
        self.found: bool = None


class InputImage:
    def __init__(self, filename):
        path = r'C:\Users\gimesia\Documents\PROJEKT\zebrafish_pipenv\src\images'  # NEED TO BE CHANGED IF RAN FROM ANOTHER COMPUTER
        path = path + "\\" + filename

        self.og: np.ndarray = cv.imread(path)
        self.processed: np.ndarray = cv.imread(path, 0)  # Already processes it to gray
        self.binary: np.ndarray = np.zeros_like(self.og.shape)
        self.height: int = 0
        self.width: int = 0
        self.well_props: WellProperties = WellProperties()
        self.fish_props: FishProperties = FishProperties()

        try:
            self.set_size()
        except():
            raise Exception("Image loading failed")

    def set_size(self):
        self.height = self.og.shape[0]
        self.width = self.og.shape[1]

    def size(self) -> tuple[int, int]:
        return self.height, self.width


EXAMPLE_IMG = InputImage("zf2.jpg")

if __name__ == '__main__':
    img = EXAMPLE_IMG
    print(img.size())
