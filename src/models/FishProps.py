from src.models import BoundingBox, Mask


class FishProperties:
    def __init__(self):
        self.bounding_box: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.rotated: bool = False
        self.container = None
        self.mod_cont = None

        self.is_fish: bool = None
