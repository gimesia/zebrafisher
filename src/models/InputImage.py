import cv2 as cv
import czifile
import numpy as np

from src.models.WellProps import WellProperties
from src.models.FishProps import FishProperties


class InputImage:
    def __init__(self, filename: str):
        import os

        path = os.path.dirname(__file__)  # r'src/images'  # NEED TO BE CHANGED IF RAN FROM ANOTHER COMPUTER
        path = path + "\\images\\" + filename

        if filename.split(".")[1] == "czi":
            self.og: np.ndarray = czifile.imread(path)[0, :, :, 0]
            self.processed: np.ndarray = self.og
        else:
            self.og: np.ndarray = cv.imread(path, 0)  # Already processes it to gray
            self.processed: np.ndarray = self.og

        self.binary: np.ndarray = np.zeros_like(self.processed)

        self.height: int = 0
        self.width: int = 0

        self.well_props: WellProperties = WellProperties()
        self.fish_props: FishProperties = FishProperties()

        try:
            self._set_size()
        except():
            raise Exception("Image loading failed")

    def _set_size(self):
        self.height = self.og.shape[0]
        self.width = self.og.shape[1]

    def size(self) -> tuple[int, int]:
        return self.height, self.width


EXAMPLE_IMG = InputImage("zf1.jpg")

if __name__ == '__main__':
    pass
