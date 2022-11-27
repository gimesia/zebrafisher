import cv2 as cv
import czifile
import numpy as np
import os

from src.models.Measurements import Measurements
from .WellProps import WellProperties
from .FishProps import FishProperties


class InputImage:
    def __init__(self, filename: str):
        """
        OLD!!!
        path = os.path.dirname(__file__)  # r'src/images'  # NEED TO BE CHANGED IF RAN FROM ANOTHER COMPUTER
        path = path + "\\images\\in\\" + filename
        """
        self.name = filename
        cwd = os.path.abspath('..')
        path = os.path.join(cwd, 'src', 'images', 'in', filename)

        print(f"Reading in file from:\n{path}")

        if filename.split(".")[1] == "czi":
            self.og: np.ndarray = czifile.imread(path)[0, :, :, 0]
            self.processed: np.ndarray = self.og
        else:
            self.og: np.ndarray = cv.imread(path, 0)  # Already processes it into grayscale
            self.processed: np.ndarray = self.og

        self.height: int = 0
        self.width: int = 0

        self.well_props: WellProperties = WellProperties()
        self.fish_props: FishProperties = FishProperties()
        self.measurements: Measurements = Measurements()

        self.success: bool = False

        try:
            self.height = self.og.shape[0]
            self.width = self.og.shape[1]
        except():
            print("Image loading failed")


if __name__ == '__main__':
    pass
