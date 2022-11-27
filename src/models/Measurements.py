from src.models import BoundingBox


class Measurements:

    def __init__(self):
        self.resolution = None
        self.head_to_tail_length: int = None
        self.head_endpoint: (int, int) = None
        self.tail_endpoint: (int, int) = None
        self.orientation: float = None
        self.eye1_diameter_major: int = None
        self.eye2_diameter_major: int = None
        self.well_roi: BoundingBox = None
        self.fish_roi: BoundingBox = None

    def calculate_resolution(self, r: int) -> float:
        self.resolution = 7.0 / (r * 2.0)
        return self.resolution
