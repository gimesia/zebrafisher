import cv2 as cv


class InputImage:
    def __init__(self, filename):
        self.og = cv.imread(filename)
        self.processed = cv.imread(filename, 0)
        self.height = 0
        self.width = 0
        self.wellProps = WellProperties()


class WellProperties:
    def __init__(self):
        self.min_circle = None
        self.max_circle = None
        self.center = None
        self.radius = None
        self.foundWell = None
