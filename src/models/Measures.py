from src.models import BoundingBox


class Measures:
    def __int__(self):
        self.well_roi: BoundingBox = None
        self.fish_roi: BoundingBox = None
        self.head_to_tail_length: int = None
        self.eye_diameter_mean: int = None
        self.eye_diameter_major: int = None
        self.eye_diameter_minor: int = None
        self.head_endpoint: (int, int) = None
        self.tail_endpoint: (int, int) = None
