import cv2 as cv
import numpy as np


class InputImage:
    def __init__(self, filename):
        self.og: np.ndarray = cv.imread(filename)
        self.processed: np.ndarray = cv.imread(filename, 0)
        self.height: int = 0
        self.width: int = 0
        self.well_props: WellProperties = WellProperties()


class WellProperties:
    def __init__(self):
        self.min_circle: int = None
        self.max_circle: int = None
        self.center: tuple[int, int] = None
        self.radius: int = None
        self.found_well: bool = None
        self.mask: np.ndarray = None
        self.bounding_box: BoundingBox = BoundingBox()


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
