from src.models import BoundingBox, Mask


class FishProperties:
    def __init__(self):
        self.bounding_box: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.rotated: bool = False
        self.is_fish: bool = None

        self.contours: Contours = Contours()


class Contours:
    def __init__(self):
        self.body = None
        self.spine = None
        self.eyes = None
