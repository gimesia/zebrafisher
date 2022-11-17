from src.models import BoundingBox, Mask


class FishProperties:
    def __init__(self):
        self.bounding_box_og: BoundingBox = BoundingBox()
        self.bounding_box_well: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.cropped_og = None  # Image of the original input image, but cropped to display only the fish

        self.rotated: bool = False
        self.has_fish: bool = None

        self.contours: Contours = Contours()


class Contours:
    def __init__(self):
        self.body = None
        self.spine = None
        self.eyes = None
