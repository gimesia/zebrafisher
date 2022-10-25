from src.models import BoundingBox, Mask


class WellProperties:
    def __init__(self):
        self.center: tuple[int, int] = None
        self.radius: int = None

        self.bounding_box: BoundingBox = BoundingBox()
        self.mask: Mask = Mask()

        self.has_well: bool = False
