import cv2 as cv
import numpy as np

from src.models.WellProps import WellProperties
from src.models.FishProps import FishProperties
from src.terminal_msg import show_img, msg


class InputImage:
    def __init__(self, filename):
        import os
        print(os.path.dirname(__file__))

        path = os.path.dirname(__file__)  # r'src/images'  # NEED TO BE CHANGED IF RAN FROM ANOTHER COMPUTER
        path = path + "\\images\\" + filename
        print(path)

        self.og: np.ndarray = cv.imread(path)
        self.processed: np.ndarray = cv.imread(path, 0)  # Already processes it to gray
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


EXAMPLE_IMG = InputImage("zf2.jpg")

if __name__ == '__main__':
    pass
