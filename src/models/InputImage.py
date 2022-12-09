import os

import cv2 as cv
import czifile
import numpy as np

from src.models.Measurements import Measurements
from .FishProps import FishProperties
from .Timer import Timer
from .WellProps import WellProperties


class InputImage:
    def __init__(self, filename: str):
        self.name = filename

        # Generating path from filename
        cwd = os.getcwd()
        path = os.path.abspath('..')
        if path.split()[-1] != 'src':
            path = os.path.join(path, 'src')
        path = os.path.join(path, 'images', 'in', filename)

        fileformat: str = filename.split(".")[-1].lower()  # Gets file format if item is a file

        if fileformat == "czi":
            self.og: np.ndarray = czifile.imread(path)[0, :, :, 0]
            self.processed: np.ndarray = self.og
        elif fileformat == "png" or fileformat == "tiff" or fileformat == "jpg":
            self.og: np.ndarray = cv.imread(path, 0)  # Already processes it into grayscale
            self.processed: np.ndarray = self.og

        self.height: int = 0
        self.width: int = 0

        self.well_props: WellProperties = WellProperties()
        self.fish_props: FishProperties = FishProperties()
        self.measurements: Measurements = Measurements()

        self.success: bool = False

        self.timer = Timer()
        try:
            self.height = self.og.shape[0]
            self.width = self.og.shape[1]
        except():
            print("Image loading failed")
