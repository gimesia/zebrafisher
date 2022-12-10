import numpy as np

from .BoundingBox import BoundingBox
from .Mask import Mask


class FishProperties:
    def __init__(self):
        self.bounding_box_og: BoundingBox = BoundingBox()
        self.bounding_box_well: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.cropped_og: np.ndarray = None  # Image of the original input image, but cropped to display only the fish

        self.rotated: bool = False
        self.head: str = None
        self.eyes: np.ndarray = None

        self.has_fish: bool = None
        self.has_eyes: bool = None
