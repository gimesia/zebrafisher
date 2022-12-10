from .BoundingBox import BoundingBox
from .Mask import Mask


class WellProperties:
    def __init__(self):
        self.center: (int, int) = None
        self.radius: int = None

        self.bounding_box: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.has_well: bool = False
